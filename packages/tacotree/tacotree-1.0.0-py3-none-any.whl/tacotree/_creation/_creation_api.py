# Copyright (C) 2024 Matthias Nadig

import torch.nn as nn

from ._modules import add_module
from . import Config, Model
from . import _modules


def create_model(sequences, workflow, groups=None, debug=False):
    """
    Sequences specify each branch as sequential sub-model.
    Workflow specifies how inputs are passed from branch to branch.
    """
    config = _create_config(sequences=sequences, workflow=workflow, groups=groups)
    model = _create_from_config(config=config, debug=debug)
    return model


def create_config(sequences, workflow, groups=None):
    config = _create_config(sequences=sequences, workflow=workflow, groups=groups)
    return config


def create_from_config(config, debug=False):
    return _create_from_config(config=config, debug=debug)


def _create_config(sequences, workflow, groups):
    config = Config(sequences=sequences, workflow=workflow, groups=groups)
    return config


def _create_from_config(config, debug):
    module_dict = dict()
    for seq_name, seq_modules in config.sequences.items():
        # Check if sequence has multiple inputs at some point of the workflow
        # (as of now, we need to know this for choosing nn.Sequential or not)
        flag_per_flow = []
        for flow in config.workflow:
            for i, seq_names_check in enumerate(flow):
                if i != 0:
                    if isinstance(seq_names_check, str):
                        seq_names_check = [seq_names_check]
                    if seq_name in seq_names_check:
                        seq_names_inputs = flow[i-1]
                        if not isinstance(seq_names_inputs, str) and len(seq_names_inputs) > 1:
                            has_multiple_inputs = True
                            break
            else:
                has_multiple_inputs = False
            flag_per_flow.append(has_multiple_inputs)
        has_multiple_inputs = any(flag_per_flow)

        # Create the sequence
        module_dict[seq_name] = _modules.create_sequence(modules=seq_modules, debug=debug,
                                                         has_multiple_inputs=has_multiple_inputs)
    sequences = nn.ModuleDict(module_dict)

    model = Model(config=config, sequences=sequences, debug=debug)

    return model
