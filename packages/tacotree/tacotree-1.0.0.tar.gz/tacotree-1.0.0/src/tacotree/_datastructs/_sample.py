# Copyright (C) 2024 Matthias Nadig

import numpy as np
import torch

from ._base_data import BaseData
from . import _annotations


def as_sample(data, n_dims, annotations=None, limits=None):
    return _as_sample(data=data, n_dims=n_dims, annotations=annotations, limits=limits, constructor=Sample)


def as_sample_with_channels(data, n_dims, annotations=None, limits=None):
    return _as_sample(data=data, n_dims=n_dims, annotations=annotations, limits=limits, constructor=SampleChannels)


def _as_sample(constructor, data, n_dims, annotations=None, limits=None):
    # Make sure inputs are of correct type
    if not isinstance(n_dims, (int, float)) or n_dims != int(n_dims):
        raise TypeError(f'Expected integer for number of dimensions, got {n_dims} (type: {type(n_dims)})')

    if not isinstance(data, torch.Tensor):
        data = np.asarray(data)
        data = torch.from_numpy(data)
        _annotations.raise_if_not_none_or_iterable_of_annotations(annotations)

    # Data should be in the format (channels, dim 1, dim 2, ..., dim n)
    # Note: Shape can also be (,). In this case, n_dim must be -1 to work seamlessly with batch creation.
    if data.ndim != 1 + n_dims:
        raise ValueError(f'Got data with shape {data.shape} for {n_dims}-dimensional data')

    return constructor(data=data, annotations=annotations, limits=limits)


class Sample(BaseData):
    def __init__(self, data, annotations, limits=None):
        super().__init__(data=data, annotations=annotations)
        self._shape = self._data.shape
        self._n_axes = len(self._shape)
        self._limits = None if limits is None else np.array(limits)

    def set_data(self, data):
        """ CAVEAT! Should only be used if modified data has same properties """
        if data.shape != self._data.shape or data.dtype != self._data.dtype:
            raise ValueError(f'Trying to set not matching data (old/new): {self._data.shape} != {data.shape}, {self._data.dtype} != {data.dtype}')
        self._data = data
        return self

    def shape(self):
        return self._shape

    def n_axes(self):
        return self._n_axes

    def limits(self):
        return self._limits

    def set_limits(self, limits):
        self._limits = limits
        return self


class SampleChannels(Sample):
    def __init__(self, data, annotations, limits=None):
        super().__init__(data=data, annotations=annotations, limits=limits)
        self._n_channels = self._data.shape[0]
        self._grid_shape = self._data.shape[1:]
        self._n_dims = len(self._grid_shape)

    def n_channels(self):
        return self._n_channels

    def n_dims(self):
        return self._n_dims

    def grid_shape(self):
        return self._grid_shape
