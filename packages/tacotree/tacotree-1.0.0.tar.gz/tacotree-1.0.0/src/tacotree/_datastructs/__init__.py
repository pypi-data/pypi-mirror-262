# Copyright (C) 2024 Matthias Nadig

from ._sample import as_sample, as_sample_with_channels
from ._sample import Sample, SampleChannels
from ._batch import as_batch, as_batch_with_channels
from ._batch import Batch
from ._batch import BatchSingleTensor, BatchFlexShape
from ._batch import BatchChannelMatrix, BatchChannelsSingleTensor, BatchChannelsFlexGrid
from ._array import as_array, Array

from ._annotations import Annotation, raise_if_not_none_or_iterable_of_annotations
from ._annotations import as_label, Label
from ._annotations import as_bounds, Bounds
from ._annotations import as_semantic_map_overlapping, as_semantic_labelmap
from ._annotations import as_instance_map_overlapping, as_instance_labelmap
from ._annotations import SegmentationMap, SegmentationMapMultiClass
from ._annotations import SemanticMapOverlapping, SemanticLabelmap
from ._annotations import InstanceMapOverlapping, InstanceLabelmap
