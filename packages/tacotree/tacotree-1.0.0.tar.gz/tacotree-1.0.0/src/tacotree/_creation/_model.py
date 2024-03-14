# Copyright (C) 2024 Matthias Nadig

import numpy as np

import torch.nn as nn

from .. import Batch
from ._modules import Input, Output


class Model(nn.Module):
    def __init__(self, config, sequences, debug=False):
        super().__init__()
        self._config = config
        self._debug = debug

        self._seq = sequences
        flows = self._config.workflow
        assert isinstance(self._seq, nn.ModuleDict) and isinstance(flows, list)

        n_flows = len(flows)
        self._active_flows = np.zeros(n_flows, dtype=int)
        self._is_any_flow_explicitly_activated = False

        # Check if inputs are available for all nodes of the model
        outputs_available = []
        for flow in flows:
            for i, seq_name in enumerate(flow):
                if i == 0:
                    # First sequence of current workflow, check if all inputs are available
                    if isinstance(seq_name, str):
                        seq_name = [seq_name]
                    for input_name in seq_name:
                        is_input_given_or_processed = isinstance(self._seq[input_name], Input) or input_name in outputs_available
                        if not is_input_given_or_processed:
                            raise RuntimeError(
                                f'Given workflow does not allow to process "{input_name}" before required.\n\n' +
                                f'Outputs available:\n{outputs_available}\n\n' +
                                f'Workflow:\n{flows}'
                            )
                else:
                    # This sequence is not the first of current workflow, thus the sequence will have its inputs
                    # provided by the previous sequence of the current workflow
                    if seq_name not in outputs_available:
                        # First time, the current sequence produces an output in any of the workflows
                        outputs_available.append(seq_name)

        self._input_names = []
        self._output_names = []
        for seq_name, seq in self._seq.items():
            if isinstance(seq, Input):
                self._input_names.append(seq_name)
            elif isinstance(seq, Output):
                self._output_names.append(seq_name)
    
    def get_config(self):
        """ Returns config object of this model """
        return self._config

    def get_sequence_names(self):
        """ Returns list of sequence names """
        return list(self._seq.keys())

    def get_sequence(self, name):
        """ Returns sequence by given name """
        return self._seq[name]

    def get_input_names(self):
        """ Returns input names """
        return self._input_names

    def get_output_names(self):
        """ Returns output names """
        return self._output_names

    def clone(self, which=None):
        """ Clones a subgraph of the model (per default the full model) """
        from ._creation_api import create_from_config, create_model
        if which is None:
            # Clone full model
            # 1st: Use config to allocate new tensors for weights
            # 2nd: Copy state dict
            model_cloned = create_from_config(config=self.get_config(), debug=self._debug)
            model_cloned.load_state_dict(self.state_dict())
        else:
            # Clone subgraph of model, check which groups are to be cloned
            if isinstance(which, str):
                groups_clone = [which]
            elif hasattr(which, '__iter__') and all([isinstance(group, str) for group in which]):
                groups_clone = list(which)
            else:
                str_e = \
                    f'Expected string or iterable of strings representing group names, ' + \
                    f'got {type(which)} (value: {which})'
                raise TypeError(str_e)

            # Check if all specified groups exist
            groups_available = self._config.groups
            if not all([group in groups_available for group in groups_clone]):
                str_e = \
                    f'At least one requested group not in group names --> ' + \
                    f'requested {groups_clone}, found {list(groups_available.keys())}'
                raise ValueError(str_e)

            # Get groups, workflows and sequences to be cloned
            groups_clone = {
                group: indices_seq for group, indices_seq in groups_available.items()
                if group in groups_clone
            }
            workflow_clone = [
                sequences for i, sequences in enumerate(self._config.workflow)
                if any([i in indices_seq for _, indices_seq in groups_clone.items()])
            ]
            sequences_clone = {
                name_seq: seq for name_seq, seq in self._config.sequences.items()
                if any([
                    (
                        (name_seq == sequences[0] if isinstance(sequences[0], str) else name_seq in sequences[0]) or
                        name_seq in sequences[1:]
                    ) for i, sequences in enumerate(workflow_clone)
                ])
            }

            # Create new model and copy state dict of all required sequences
            model_cloned = create_model(
                sequences=sequences_clone, workflow=workflow_clone,
                groups=groups_clone, debug=self._debug)
            for sequence_name in model_cloned.get_sequence_names():
                sequence_new = model_cloned.get_sequence(sequence_name)
                sequences_old = self.get_sequence(sequence_name)
                sequence_new.load_state_dict(sequences_old.state_dict())

        return model_cloned

    def active_workflows(self, which):
        """
        Set active workflows explicitly
        If this method is not called, all workflows will be active per default.
        This method will deactivate the ones not explicitly activated here.
        Use in a with-statement, e.g.:
        with model.active_workflows([0, 1, 5, 6]):
            outputs = model(...)
        """
        if isinstance(which, str):
            if which == 'all':
                indices = np.arange(len(self._config.workflow))
            else:
                if which not in self._config.groups:
                    str_e = f'Group name "{which}" not available: {self._config.groups.keys()}'
                    raise ValueError(str_e)
                indices = self._config.groups[which]
        elif hasattr(which, '__iter__') and all([np.issubdtype(type(index), np.integer) for index in which]):
            indices = which
        else:
            str_e = f'Argument bad, should be indices or group name, got: type = {type(which)}, value = {which}'
            raise ValueError(str_e)
        indices = np.asarray(indices, dtype=int)
        return _WorkflowSwitch(self._activate_workflows, self._deactivate_workflows, indices)

    def forward(self, **inputs):
        """
        Forward pass of PyTorch modules
        A bit unusual as inputs should be given as keyword arguments.
        """
        # All inputs should be of batch type
        if any([not isinstance(value, Batch) for _, value in inputs.items()]):
            raise TypeError('All inputs must be of batch type, got {}'.format([
                type(value) for _, value in inputs.items()
            ]))

        # Dictionary that will contain model outputs
        outputs = dict()

        # Process all model branches in right order
        outputs_each_node = dict()
        flows = self._config.workflow
        for index_flow, flow in enumerate(flows):
            # Check if current workflow is deactivated
            if not self._is_workflow_active(index_flow):
                continue

            # Process all nodes of current workflow
            for i in range(1, len(flow)):
                seq_name_inputs = flow[i-1]
                seq_name_process = flow[i]

                if isinstance(seq_name_inputs, str):
                    seq_name_inputs = [seq_name_inputs]

                # Get inputs for current sequence either from this function's arguments or from other sequence's output
                inputs_sequence = []
                for input_name in seq_name_inputs:
                    if isinstance(self._seq[input_name], Input):
                        # TODO: Make sure that input sequence is not run redundantly
                        input_retrieved = self._seq[input_name](inputs[input_name])
                        input_current = input_retrieved
                    else:
                        input_current = outputs_each_node[input_name]
                    inputs_sequence.append(input_current)

                # Get the next sequence/model branch
                sequence = self._seq[seq_name_process]

                # Set a breakpoint, if debugging is enabled
                # Note:
                # Debugging can be enabled when creating or loading a model. This breakpoint does not require
                # a debugger to be specifically run (e.g. as in PyCharm) and will enter the debug mode.
                if self._debug:
                    breakpoint()

                # Run the current sequence/model branch
                output_current_node = sequence(*inputs_sequence)

                # Store transient output of each node of the model
                outputs_each_node[seq_name_process] = output_current_node

                # Store the node's output in final outputs of the model, in case it ends with an output layer
                if isinstance(sequence, Output):
                    outputs.update({seq_name_process: output_current_node})

        return outputs

    def _activate_workflows(self, indices):
        self._active_flows[indices] += 1
        self._check_workflow_activation()

    def _deactivate_workflows(self, indices):
        self._active_flows[indices] -= 1
        self._check_workflow_activation()

    def _check_workflow_activation(self):
        if (self._active_flows != 0).any():
            self._is_any_flow_explicitly_activated = True

    def _is_workflow_active(self, index_flow):
        # Check if any workflows have explicitly been activated and if so, check if requested flow is deactivated
        if self._is_any_flow_explicitly_activated and not self._active_flows[index_flow]:
            is_active = False
        else:
            is_active = True
        return is_active


class _WorkflowSwitch:
    def __init__(self, fn_activate, fn_deactivate, indices):
        self._fn_activate = fn_activate
        self._fn_deactivate = fn_deactivate
        self._indices = indices

        self._fn_activate(self._indices)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._fn_deactivate(self._indices)
