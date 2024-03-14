# Copyright (C) 2024 Matthias Nadig

from ... import BatchSingleTensor, BatchFlexShape
from ._base import Module


class Input(Module):
    def __init__(self, batch_size, shape):
        super().__init__()
        if batch_size not in [None, -1] and batch_size <= 0:
            raise RuntimeError(f'batch_size must be > 0, got {batch_size}')

        batch_size = -1 if batch_size is None else batch_size
        shape = tuple([-1 if dim is None else dim for dim in shape])

        self._batch_size = batch_size
        self._shape = tuple(shape)

    def _forward(self, x):
        return self._check_input(x)

    def _check_input(self, x):
        n_samples = x.n_samples()
        shape_sample = x.sample_shape()
        if isinstance(x, BatchSingleTensor):
            pass
        elif isinstance(x, BatchFlexShape):
            if all([item != -1 for item in self._shape]):
                raise RuntimeError(f'Flex batch not allowed with fixed shape')
        else:
            raise TypeError(x)
        shape_x = (n_samples, *shape_sample)
        bad_dim = len(shape_sample) != len(self._shape)
        bad_batch_size = self._batch_size != -1 and n_samples != self._batch_size
        bad_grid_shape = any([
            (dim_target != -1 and dim_x != dim_target) for dim_x, dim_target in zip(shape_sample, self._shape)
        ])
        if bad_dim or bad_batch_size or bad_grid_shape:
            str_error = (
                f'Shape of input {tuple(shape_x)} does not match the requirement ' +
                f'{(None if self._batch_size == -1 else self._batch_size,) + self._shape}'
            )
            raise ValueError(str_error)
        return x


class Output(Module):
    def __init__(self):
        super().__init__()

    def _forward(self, *args):
        return None if len(args) == 0 else (args[0] if len(args) == 1 else args)
