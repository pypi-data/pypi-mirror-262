# Copyright (C) 2024 Matthias Nadig

import torch

from ._base import Module


class Add(Module):
    def __init__(self):
        super().__init__()

    def _forward(self, *args):
        x = torch.add(*[arg.data() for arg in args])
        return self._as_batch(data=x, annotations=None, limits=None)
