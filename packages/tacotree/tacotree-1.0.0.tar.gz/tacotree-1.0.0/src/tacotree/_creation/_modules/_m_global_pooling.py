# Copyright (C) 2024 Matthias Nadig

import torch
import torch.nn.functional as F

from ._base import Module


_VECTORIZE = False


class GlobalPooling(Module):
    def __init__(self, fn_pooling, n_dims, n_features_per_channel, vectorize):
        super().__init__()
        self._fn_pooling = fn_pooling
        if isinstance(n_dims, int):
            self._n_dims = n_dims
        else:
            raise TypeError(f'Expected integer, got value of type {type(n_dims)} (value: {n_dims})')
        self.n_features_per_channel = n_features_per_channel
        self._vectorize = vectorize

    def _forward(self, x):
        data = x.data()
        data = self._fn_pooling(data, n_dims=self._n_dims)
        if not self._vectorize:
            data = data.view((-1,)*len(data.shape) + (self.n_features_per_channel,))
        x = self._as_batch_with_channels(data=data, annotations=None, limits=None)
        return x


class GlobalAverage(GlobalPooling):
    def __init__(self, n_dims, vectorize=_VECTORIZE):
        super().__init__(fn_pooling=_get_global_average, n_dims=n_dims, n_features_per_channel=1, vectorize=vectorize)


class GlobalMax(GlobalPooling):
    def __init__(self, n_dims, vectorize=_VECTORIZE):
        super().__init__(fn_pooling=_get_global_maximum, n_dims=n_dims, n_features_per_channel=1, vectorize=vectorize)


def _get_global_average(x, n_dims):
    size_out = (1,) * n_dims

    if n_dims == 1:
        x = F.adaptive_avg_pool1d(x, size_out)
    elif n_dims == 2:
        x = F.adaptive_avg_pool2d(x, size_out)
    elif n_dims == 3:
        x = F.adaptive_avg_pool3d(x, size_out)
    else:
        raise ValueError(n_dims)

    for _ in range(n_dims):
        x = torch.squeeze(x, -1)
    return x


def _get_global_maximum(x, n_dims):
    size_out = (1,) * n_dims

    if n_dims == 1:
        x = F.adaptive_max_pool1d(x, size_out)
    elif n_dims == 2:
        x = F.adaptive_max_pool2d(x, size_out)
    elif n_dims == 3:
        x = F.adaptive_max_pool3d(x, size_out)
    else:
        raise ValueError(n_dims)

    for _ in range(n_dims):
        x = torch.squeeze(x, -1)
    return x
