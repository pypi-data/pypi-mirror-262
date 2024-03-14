# Copyright (C) 2024 Matthias Nadig

import numpy as np
import torch

from ._base_data import BaseData
from ._sample import as_sample, Sample
from ._annotations import raise_if_not_none_or_iterable_of_annotations


def as_batch(samples, annotations=None, limits=None):
    return _as_batch(constructor_static=BatchSingleTensor, constructor_flex=BatchFlexShape, samples=samples, annotations=annotations, limits=limits)


def as_batch_with_channels(samples, annotations=None, limits=None):
    return _as_batch(constructor_static=BatchChannelsSingleTensor, constructor_flex=BatchChannelsFlexGrid, samples=samples, annotations=annotations, limits=limits)


def _as_batch(constructor_static, constructor_flex, samples, annotations=None, limits=None):
    if not hasattr(samples, '__len__'):
        raise TypeError(samples)

    # Make sure annotations are of correct type
    if annotations is not None:
        if not hasattr(annotations, '__len__'):
            raise TypeError(f'Expected iterable with items of Annotation-type, got {annotations}')
        if len(annotations) != len(samples):
            raise ValueError(f'Expected at least one annotation for each sample, got ({len(annotations)} != {len(samples)}) --> {annotations}')
        for annotation_of_sample in annotations:
            raise_if_not_none_or_iterable_of_annotations(annotation_of_sample)

    # Make sure inputs are of correct type
    if isinstance(samples, torch.Tensor):
        batch = _from_torch(constructor=constructor_static, samples=samples, annotations=annotations, limits=limits)
    elif isinstance(samples, np.ndarray):
        batch = _from_numpy(constructor=constructor_static, samples=samples, annotations=annotations, limits=limits)
    elif all([isinstance(s, Sample) for s in samples]):
        # Use annotations from samples
        if annotations is not None:
            raise ValueError
        else:
            annotations = [s.annotations() for s in samples]

        # Expecting samples to have same limits, if no limit is given as argument
        limits_found = [None if s.limits() is None else tuple(s.limits()) for s in samples]
        if limits is None:
            limits = limits_found[0]
        else:
            if not all([limits_found[0] == limits_current for limits_current in limits_found]):
                raise ValueError(
                    f'If not limit is set explicitly, all samples must have same limits. Got: {limits_found}')
        batch = _from_samples(constructor_static=constructor_static, constructor_flex=constructor_flex, samples=samples, annotations=annotations, limits=limits)
    elif all([isinstance(s, np.ndarray) for s in samples]) or all([isinstance(s, torch.Tensor) for s in samples]):
        if annotations is not None and not (hasattr(annotations, '__iter__') and len(annotations) == len(samples)):
            raise ValueError(annotations)
        if limits is not None and not (hasattr(limits, '__iter__') and len(limits) == 2):
            raise ValueError(limits)
        n_dims = len(samples[0].shape) - 1
        if not all([len(s.shape) - 1 == n_dims for s in samples]):
            raise ValueError([s.shape for s in samples])
        samples = [
            as_sample(data=s, n_dims=n_dims) for i, s in enumerate(samples)
        ]
        batch = _from_samples(constructor_static=constructor_static, constructor_flex=constructor_flex, samples=samples, annotations=annotations, limits=limits)
    else:
        types_each_sample = [type(s) for s in samples]
        raise TypeError(f'Expected Numpy array or list with items of Sample-type, got {types_each_sample}')

    return batch


def _from_torch(constructor, samples, annotations, limits):
    return constructor(data=samples, annotations=annotations, limits=limits)


def _from_numpy(constructor, samples, annotations, limits):
    samples = torch.from_numpy(samples)
    return constructor(data=samples, annotations=annotations, limits=limits)


def _from_samples(constructor_static, constructor_flex, samples, annotations, limits):
    # Expecting samples to be of same shapes
    shape_expected = samples[0].data().shape
    is_shape_equal = all([s.data().shape == shape_expected for s in samples])
    if is_shape_equal:
        data = torch.stack([s.data() for s in samples])
        batch = constructor_static(data=data, annotations=annotations, limits=limits)
    else:
        # shape_each_sample = [s.data().shape for s in samples]
        # raise ValueError(f'Expected all shapes to be equal, got shapes {shape_each_sample}')
        # warnings.warn('Batch with flexible shape is created. This should only happen during debugging.')
        data = [s.data() for s in samples]
        batch = constructor_flex(data=data, annotations=annotations, limits=limits)

    return batch


class Batch(BaseData):
    def __init__(self, data, annotations, limits, sample_shape):
        super().__init__(data=data, annotations=annotations)
        self._shape_sample = sample_shape
        self._limits = limits
        self._n_axes = len(self._shape_sample)
        self._n_samples = len(self._data)

    def n_samples(self):
        return self._n_samples

    def n_axes(self):
        return self._n_axes

    def sample_shape(self):
        return self._shape_sample

    def limits(self):
        return self._limits

    def set_limits(self, limits):
        self._limits = limits
        return self


class BatchSingleTensor(Batch):
    def __init__(self, data, annotations=None, limits=None):
        # n_channels = None if len(data.shape) == 1 else data.shape[1]
        sample_shape = data.shape[1:]
        super().__init__(data=data, annotations=annotations, limits=limits, sample_shape=sample_shape)  # , n_channels=n_channels)

    def set_data(self, data):
        """ CAVEAT! Should only be used if modified data has same properties """
        if data.shape != self._data.shape or data.dtype != self._data.dtype:
            raise ValueError(f'Trying to set not matching data (old/new): {self._data.shape} != {data.shape}, {self._data.dtype} != {data.dtype}')
        self._data = data
        return self


class BatchFlexShape(Batch):
    def __init__(self, data, annotations=None, limits=None):
        # n_dims = len(data[0].shape) - 1
        # n_channels = None if len(data[0].shape) == 0 else data[0].shape[0]
        # for sample in data:
        #     if len(sample.shape) - 1 != n_dims or (None if len(sample.shape) == 0 else sample.shape[0]) != n_channels:
        #         raise ValueError([s.shape for s in data])
        # n_dims = max(0, n_dims)  # could be -1 if sample is a scalar
        sample_shape = _get_flexible_shape(data)
        super().__init__(data=data, annotations=annotations, limits=limits, sample_shape=sample_shape)

    def set_data(self, data):
        """ CAVEAT! Should only be used if modified data has same properties """
        raise RuntimeError('Data modification not implemented yet')

    def as_type(self, dtype):
        self._data = [sample.type(dtype) for sample in self._data]
        return self

    def to(self, *args, **kwargs):
        self._data = [sample.to(*args, **kwargs) for sample in self._data]
        return self


class BatchChannelMatrix:
    def __init__(self, n_channels, grid_shape, **kwargs):
        super().__init__(**kwargs)  # required for multi-inheritance
        self._grid_shape = grid_shape
        self._n_dims = len(self._grid_shape)
        self._n_channels = n_channels

    def n_channels(self):
        return self._n_channels

    def n_dims(self):
        return self._n_dims

    def grid_shape(self):
        return self._grid_shape


class BatchChannelsSingleTensor(BatchChannelMatrix, BatchSingleTensor):
    def __init__(self, data, annotations=None, limits=None):
        grid_shape = data.shape[2:]
        # n_channels = None if len(data.shape) == 1 else data.shape[1]
        n_channels = data.shape[1]
        super().__init__(
            n_channels=n_channels, grid_shape=grid_shape,
            data=data, annotations=annotations, limits=limits)


class BatchChannelsFlexGrid(BatchChannelMatrix, BatchFlexShape):
    def __init__(self, data, annotations=None, limits=None):
        sample_shape = _get_flexible_shape(data)
        n_channels = sample_shape[0]
        grid_shape = sample_shape[1:]
        super().__init__(
            n_channels=n_channels, grid_shape=grid_shape,
            data=data, annotations=annotations, limits=limits)


def _get_flexible_shape(data):
    shape = [
        -1 if len(np.unique(column)) != 1 else column[0] for column in np.asarray([
            sample.shape for sample in data
        ]).transpose()
    ]
    return shape
