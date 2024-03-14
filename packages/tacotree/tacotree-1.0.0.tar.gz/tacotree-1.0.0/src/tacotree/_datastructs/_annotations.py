# Copyright (C) 2024 Matthias Nadig

import numpy as np
import ndbounds


def as_label(label):
    return Label(label=label)


def as_bounds(bounds, labels):
    return Bounds(bounds=bounds, labels=labels)


def as_semantic_map_overlapping(segmentation_map, labels, n_dims):
    _check_input_types(segmentation_map=segmentation_map, labels=labels, dtype_required=np.bool_)
    _check_grid_shape(segmentation_map=segmentation_map, n_dims=n_dims, n_leading=1)
    return SemanticMapOverlapping(segmentation_map=segmentation_map, labels=labels)


def as_semantic_labelmap(segmentation_map, labels, n_dims):
    _check_input_types(segmentation_map=segmentation_map, labels=labels, dtype_required=np.integer)
    _check_grid_shape(segmentation_map=segmentation_map, n_dims=n_dims, n_leading=0)
    return SemanticLabelmap(segmentation_map=segmentation_map, labels=labels)


def as_instance_map_overlapping(segmentation_map, labels, n_dims):
    _check_input_types(segmentation_map=segmentation_map, labels=labels, dtype_required=np.bool_)
    _check_grid_shape(segmentation_map=segmentation_map, n_dims=n_dims, n_leading=2)
    return InstanceMapOverlapping(segmentation_map=segmentation_map, labels=labels)


def as_instance_labelmap(segmentation_map, labels, n_dims):
    _check_input_types(segmentation_map=segmentation_map, labels=labels, dtype_required=np.integer)
    _check_grid_shape(segmentation_map=segmentation_map, n_dims=n_dims, n_leading=1)
    return InstanceLabelmap(segmentation_map=segmentation_map, labels=labels)


def _check_input_types(segmentation_map, labels, dtype_required):
    if not isinstance(segmentation_map, np.ndarray) or not np.issubdtype(segmentation_map.dtype, dtype_required):
        str_e = f'Expected segmentation_map to be array of type {dtype_required}, got {type(segmentation_map)}'
        if isinstance(segmentation_map, np.ndarray) and not np.issubdtype(segmentation_map.dtype, dtype_required):
            str_e += f' of type {segmentation_map.dtype}'
        raise TypeError(str_e)
    if not isinstance(labels, np.ndarray):
        str_e = f'Expected labels to be array, got {type(labels)}'
        raise TypeError(str_e)


def _check_grid_shape(segmentation_map, n_dims, n_leading):
    if segmentation_map.ndim - n_leading != n_dims:
        str_e = \
            f'Bad shape {segmentation_map.shape} for this kind of segmentation map assuming a {n_dims}-dimensional grid'
        raise ValueError(str_e)


def raise_if_not_none_or_iterable_of_annotations(annotations):
    if annotations is not None and (not hasattr(annotations, '__iter__') or
                                    not all([isinstance(ann, Annotation) for ann in annotations])):
        raise TypeError(f'Annotations should be a list of Annotation-objects, got {annotations}')


class Annotation:
    """
    Base class for annotations
    """
    def __init__(self):
        pass


class Label(Annotation):
    """
    Label (could be of any type: integer, string, ...)
    """
    def __init__(self, label):
        super().__init__()
        self._label = label

    def label(self):
        return self._label


class Bounds(Annotation):
    """
    Bounds (N-dimensional, start and end of objects) with label
    """
    def __init__(self, bounds, labels):
        super().__init__()
        ndbounds.raise_if_not_ndbounds(bounds=bounds)

        self._bounds = bounds
        self._labels = np.asarray(labels)

    def bounds(self):
        return self._bounds

    def labels(self):
        return self._labels

    def n_objects(self):
        return len(self._labels)


class SegmentationMap(Annotation):
    """
    Base class for various kinds of segmentation maps
    """
    def __init__(self, segmentation_map, labels, n_dims):
        super().__init__()
        assert isinstance(segmentation_map, np.ndarray)
        assert isinstance(labels, np.ndarray)
        self._map = segmentation_map
        self._labels = labels
        self._n_dims = n_dims

    def n_dims(self):
        """ Returns number of dimensions of grid """
        return self._n_dims

    def shape(self):
        """ Returns shape of grid """
        return self._map.shape[-self._n_dims:]


class SegmentationMapMultiClass(SegmentationMap):
    """
    Base class for various kinds of segmentation maps given multiple classes
    """
    def __init__(self, segmentation_map, labels, n_dims):
        super().__init__(segmentation_map=segmentation_map, labels=labels, n_dims=n_dims)

    def n_classes(self):
        return len(self._labels)

    def get_classes(self):
        return self._labels

    def semantic_map(self, label):
        """
        Returns semantic map for a given label
        Shape: (dim 1, ..., dim N)
        """
        return self._semantic_map(label)

    def _index_of_label(self, label):
        return np.argwhere(self._labels == label).flatten()[0]

    def _semantic_map(self, label):
        raise NotImplementedError


class SemanticMapOverlapping(SegmentationMapMultiClass):
    """
    Semantic segmentation map
    Maps for all classes are stacked as boolean masks.
    Shape: (classes, dim 1, ..., dim N)
    """
    def __init__(self, segmentation_map, labels):
        n_dims = segmentation_map.ndim - 1
        super().__init__(segmentation_map=segmentation_map, labels=labels, n_dims=n_dims)

    def _semantic_map(self, label):
        semantic_map = self._map[self._index_of_label(label)]
        return semantic_map


class SemanticLabelmap(SegmentationMapMultiClass):
    """
    Semantic segmentation map
    Single map that encodes classes using integers.
    Shape: (dim 1, ..., dim N)
    """
    def __init__(self, segmentation_map, labels):
        n_dims = segmentation_map.ndim
        super().__init__(segmentation_map=segmentation_map, labels=labels, n_dims=n_dims)

    def _semantic_map(self, label):
        semantic_map = self._map == self._index_of_label(label)
        return semantic_map

    def semantic_labelmap(self):
        return self._map


class InstanceMapOverlapping(SegmentationMapMultiClass):
    """
    Instance segmentation map
    Maps for all classes are stacked as boolean masks.
    Boolean type with shape: (classes, instances, dim 1, ..., dim N)
    """
    def __init__(self, segmentation_map, labels):
        n_dims = segmentation_map.ndim - 2
        super().__init__(segmentation_map=segmentation_map, labels=labels, n_dims=n_dims)
    
    def _semantic_map(self, label):
        semantic_map = self._map[self._index_of_label(label)].any(axis=0)
        return semantic_map


class InstanceLabelmap(SegmentationMapMultiClass):
    """
    Instance segmentation map
    Maps for all classes are stacked and encode instances using integers.
    Integer type with shape: (classes, dim 1, ..., dim N)
    """
    def __init__(self, segmentation_map, labels):
        n_dims = segmentation_map.ndim - 1
        super().__init__(segmentation_map=segmentation_map, labels=labels, n_dims=n_dims)
    
    def _semantic_map(self, label):
        semantic_map = self._map[self._index_of_label(label)].astype(bool)
        return semantic_map
