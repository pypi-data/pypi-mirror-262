# Copyright (C) 2024 Matthias Nadig

import numpy as np
import torch

from ._base_data import BaseData


def as_array(data, annotations=None):
    data = np.asarray(data)
    data = torch.from_numpy(data)
    return Array(data=data, annotations=annotations)


class Array(BaseData):
    def __init__(self, data, annotations):
        super().__init__(data=data, annotations=annotations)

    def shape(self):
        return self._data.shape
