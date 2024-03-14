# Copyright (C) 2024 Matthias Nadig

import torch

from ._base import Module


def _axis_in_batch_dim(axis):
    """
    Checks if axis >= 0 and then adds 1, as parameters given by user should not include batch size
    Note:
        All axes should be given relating to a single sample, the batch axis (the 1st one) should be added and taken
        care of by this toolbox. Therefore, negative axes should be accepted only in special cases as in Flatten.
        To allow the usage of more dynamic negative axes, the forward function should check, if the batch axis is
        affected.
    """
    if not isinstance(axis, int) or axis < 0:
        str_e = f'Axis must be an integer >= 0, got {axis} of type {type(axis)}'
        raise RuntimeError(str_e)
    return axis + 1


class Flatten(Module):
    def __init__(self, axis_start=0, axis_end=-1):
        super().__init__()
        # Parameters given by user should not include batch size
        axis_start = _axis_in_batch_dim(axis_start)
        axis_end = axis_end if axis_end == -1 else _axis_in_batch_dim(axis_end)
        self._axis_start = axis_start
        self._axis_end = axis_end

    def _forward(self, x):
        x = x.data()
        x = torch.flatten(x, start_dim=self._axis_start, end_dim=self._axis_end)
        return self._as_batch(data=x, annotations=None, limits=None)


class Vectorize(Flatten):
    def __init__(self):
        super().__init__(axis_start=0)


class Transpose(Module):
    def __init__(self, order):
        super().__init__()
        if not hasattr(order, '__iter__'):
            raise TypeError(f'order must be an iterable, got value of type {type(order)} (value: {order})')

        # Parameters given by user should not include batch size
        order = (0,) + tuple([_axis_in_batch_dim(axis) for axis in order])
        self._order = order

    def _forward(self, x):
        x = x.data()
        x = x.permute(*self._order)
        return self._as_batch(data=x, annotations=None, limits=None)


class SwapAxes(Module):
    def __init__(self, axis1, axis2):
        super().__init__()
        # Parameters given by user should not include batch size
        axis1 = _axis_in_batch_dim(axis1)
        axis2 = _axis_in_batch_dim(axis2)
        self._axis1 = axis1
        self._axis2 = axis2

    def _forward(self, x):
        x = x.data()
        x = x.swapaxes(self._axis1, self._axis2)
        return self._as_batch(data=x, annotations=None, limits=None)


class Concat(Module):
    def __init__(self, axis):
        super().__init__()
        # Parameters given by user should not include batch size
        axis = _axis_in_batch_dim(axis)
        self._axis = axis

    def _forward(self, *args):
        args = [arg.data() for arg in args]
        x = torch.cat(args, self._axis)
        return self._as_batch(data=x, annotations=None, limits=None)


class Stack(Module):
    def __init__(self, axis):
        super().__init__()
        # Parameters given by user should not include batch size
        axis = _axis_in_batch_dim(axis)
        self._axis = axis

    def _forward(self, *args):
        args = [arg.data() for arg in args]
        x = torch.stack(args, self._axis)
        return self._as_batch(data=x, annotations=None, limits=None)


class Squeeze(Module):
    def __init__(self, axis):
        super().__init__()
        # Parameters given by user should not include batch size
        axis = _axis_in_batch_dim(axis)
        self._axis = axis

    def _forward(self, x):
        x = x.data()
        x = x.squeeze(self._axis)
        return self._as_batch(data=x, annotations=None, limits=None)


class Unsqueeze(Module):
    def __init__(self, axis):
        super().__init__()
        # Parameters given by user should not include batch size
        axis = _axis_in_batch_dim(axis)
        self._axis = axis

    def _forward(self, x):
        x = x.data()
        x = x.unsqueeze(self._axis)
        return self._as_batch(data=x, annotations=None, limits=None)


class Reshape(Module):
    def __init__(self, shape):
        super().__init__()
        if not hasattr(shape, '__iter__'):
            raise TypeError(f'shape must be an iterable, got value of type {type(shape)} (value: {shape})')
        self._shape = tuple(shape)

    def _forward(self, x):
        x = x.data()
        n_samples = len(x)
        x = x.reshape(n_samples, *self._shape)
        return self._as_batch(data=x, annotations=None, limits=None)


class View(Module):
    def __init__(self, shape):
        super().__init__()
        if not hasattr(shape, '__iter__'):
            raise TypeError(f'shape must be an iterable, got value of type {type(shape)} (value: {shape})')
        self._shape = tuple(shape)

    def _forward(self, x):
        x = x.data()
        n_samples = len(x)
        x = x.view(n_samples, *self._shape)
        return self._as_batch(data=x, annotations=None, limits=None)


class Argmax(Module):
    def __init__(self, axis=0):
        super().__init__()
        # Parameters given by user should not include batch size
        axis = _axis_in_batch_dim(axis)
        self._axis = axis

    def _forward(self, x):
        x = x.data()
        x = torch.argmax(x, self._axis)
        return self._as_batch(data=x, annotations=None, limits=None)
