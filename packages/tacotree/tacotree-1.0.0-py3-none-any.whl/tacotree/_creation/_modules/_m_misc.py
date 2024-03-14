# Copyright (C) 2024 Matthias Nadig

from ._base import Module


class DebugBreakpoint(Module):
    """ Sets breakpoints for debugging """

    def __init__(self):
        super().__init__()

    def _forward(self, *args):
        breakpoint()
        return None if len(args) == 0 else (args[0] if len(args) == 1 else args)


class PassThrough(Module):
    """ A layer that does nothing (e.g. for setting breakpoints when debugging) """

    def __init__(self):
        super().__init__()

    def _forward(self, *args):
        return None if len(args) == 0 else (args[0] if len(args) == 1 else args)


class Lambda(Module):
    """ Invokes callable in forward pass """

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def _forward(self, *args):
        return self._fn(*args)


class SelectFromTuple(Module):
    """ E.g. after LSTM layer, which has multiple outputs """

    def __init__(self, index):
        super().__init__()
        # self._index = nn.Parameter(torch.tensor(index), requires_grad=False)
        self._index = index

    def _forward(self, x_tuple):
        return x_tuple[self._index]


class TTModel(Module):
    """ A module that executes a tacotree model """

    def __init__(self, order_inputs, order_outputs, config, state_dict):
        super().__init__()
        # Import the creation function here to not run into recursive import
        from .. import create_from_config

        self._order_inputs = order_inputs
        self._order_outputs = order_outputs
        self._model = create_from_config(config=config)

        self._model.load_state_dict(state_dict)

        # self._workflow_switch = self._model.active_workflows(indices=)

    def _forward(self, *inputs):
        dict_inputs = {input_name: input_value for input_name, input_value in zip(self._order_inputs, inputs)}
        outputs = self._model(**dict_inputs)
        if len(self._order_outputs) == 1:
            ret_outputs = outputs[self._order_outputs[0]]
        else:
            ret_outputs = tuple(outputs[output_name] for output_name in self._order_outputs)
        return ret_outputs
