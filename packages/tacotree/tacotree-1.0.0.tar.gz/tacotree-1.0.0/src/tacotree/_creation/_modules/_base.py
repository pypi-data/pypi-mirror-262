# Copyright (C) 2024 Matthias Nadig

import torch.nn as nn

from ... import as_batch, as_batch_with_channels  # , BatchSingleTensor, BatchFlexGrid


class Module(nn.Module):
    """
    Every module should be of this class (network layers, preprocessing, ...) even if they are stacked in a Sequential
    """

    def __init__(self):
        super().__init__()
        self._debug = False

    def set_debug(self, debug):
        self._debug = debug
        return self

    def forward(self, *batches_in):
        batches_out = self._forward(*batches_in)

        if self._debug:
            breakpoint()

        return batches_out

    @staticmethod
    def _as_batch(data, annotations, limits):
        return as_batch(samples=data, annotations=annotations, limits=limits)

    @staticmethod
    def _as_batch_with_channels(data, annotations, limits):
        return as_batch_with_channels(samples=data, annotations=annotations, limits=limits)

    def _forward(self, *args):
        raise NotImplementedError
