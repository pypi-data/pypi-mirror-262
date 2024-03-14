# Copyright (C) 2024 Matthias Nadig

import torch.nn as nn

from ._base import Module


class SequentialBase(Module):
    def __init__(self):
        super().__init__()

    def create(self, modules, debug):
        self.set_debug(debug=debug)
        self._create(modules=modules)
        return self

    def _create(self, modules):
        """ Takes a list (simple list, not nn.ModuleList!) of tacotree Modules """
        raise NotImplementedError

    def _forward(self, *args):
        raise NotImplementedError


class SequentialSingleInput(SequentialBase):
    """ Wraps nn.Sequential """

    def __init__(self):
        super().__init__()
        self._processor = None

    def _create(self, modules):
        self._processor = nn.Sequential(*modules)

    def _forward(self, *args):
        return self._processor(*args)


class SequentialMultipleInputs(SequentialBase):
    """ Similar to nn.Sequential, but allows first module to take multiple arguments """

    def __init__(self):
        super().__init__()
        self._processors = None

    def _create(self, modules):
        self._processors = nn.ModuleList(modules)

    def _forward(self, *args):
        x = self._processors[0](*args)
        for module in self._processors[1:]:
            x = module(x)
        return x
