# Copyright (C) 2024 Matthias Nadig

import numpy as np

import torch

from ._base import Module


class CircularPad(Module):
    def __init__(self, n_dims, pad):
        super().__init__()
        self._n_dims = n_dims
        if isinstance(pad, int):
            pad = (pad,) * self._n_dims * 2
        if not (
            hasattr(pad, '__iter__') and
            len(pad) == self._n_dims * 2 and
            all([isinstance(p, int) for p in pad])
        ):
            raise TypeError(f'Padding info invalid: {pad}')
        self._pad = np.array(pad).reshape((self._n_dims, 2))

    def _forward(self, batch):
        x, annotations, limits = batch.data(), batch.annotations(), batch.limits()

        n_axes_input = x.ndim
        n_dims_pooling = self._n_dims
        n_axes_static = n_axes_input - n_dims_pooling

        shape_dims = x.shape[-n_dims_pooling:]

        slice_full = slice(0, None, 1)
        slices_static = (slice_full,) * n_axes_static

        for i in range(n_dims_pooling):
            slice_pad_right = slices_static + tuple(
                slice_full if index_dim != i else slice(0, self._pad[i, 1], 1)
                for index_dim in range(n_dims_pooling)
            )
            slice_pad_left = slices_static + tuple(
                slice_full if index_dim != i else slice(shape_dims[i]-self._pad[i, 0], shape_dims[i], 1)
                for index_dim in range(n_dims_pooling)
            )

            x = torch.cat([x, x[slice_pad_right]], dim=n_axes_static+i)
            x = torch.cat([x[slice_pad_left], x], dim=n_axes_static+i)

        # Caveat!
        # Bounding boxes and similar annotations are inaccurate after this layer in the current implementation.
        # For now, we therefore do not forward the annotations here.
        x = self._as_batch(data=x, annotations=None, limits=None)

        return x


class CircularPad1d(CircularPad):
    def __init__(self, pad):
        super().__init__(n_dims=1, pad=pad)


if __name__ == '__main__':
    a = np.array([
        [1, 2, 3, 4, 5],
        [11, 22, 33, 44, 55],
        [111, 222, 333, 444, 555],
        [1111, 2222, 3333, 4444, 555],
    ])
    t = torch.from_numpy(np.repeat(a[np.newaxis], 2, axis=0))

    print(f'Original: {t}')

    t_pad = CircularPad1d(pad=(2, 3))(t)

    print(f'Padded: {t_pad}')
