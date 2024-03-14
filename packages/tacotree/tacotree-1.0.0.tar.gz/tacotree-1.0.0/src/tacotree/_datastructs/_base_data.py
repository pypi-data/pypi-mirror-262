# Copyright (C) 2024 Matthias Nadig


class BaseData:
    def __init__(self, data, annotations):
        self._data = data
        self._ann = annotations

    def data(self):
        return self._data

    def annotations(self):
        return self._ann

    def as_type(self, dtype):
        self._data = self._data.type(dtype)
        return self

    def to(self, *args, **kwargs):
        self._data = self._data.to(*args, **kwargs)
        return self

    def enable_grad(self, requires_grad):
        self._data.requires_grad_(requires_grad)
        return self
