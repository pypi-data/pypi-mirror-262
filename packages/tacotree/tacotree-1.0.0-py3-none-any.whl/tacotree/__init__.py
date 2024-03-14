# Copyright (C) 2024 Matthias Nadig

from ._datastructs import as_sample, as_sample_with_channels
from ._datastructs import as_batch, as_batch_with_channels
from ._datastructs import as_array
from ._datastructs import as_label
from ._datastructs import as_bounds
from ._datastructs import as_semantic_map_overlapping, as_semantic_labelmap
from ._datastructs import as_instance_map_overlapping, as_instance_labelmap
from ._datastructs import Sample
from ._datastructs import Batch, BatchSingleTensor, BatchFlexShape
from ._datastructs import BatchChannelMatrix, BatchChannelsSingleTensor, BatchChannelsFlexGrid
from ._datastructs import Array
from ._datastructs import Annotation, Label, Bounds
from ._datastructs import SegmentationMap, SegmentationMapMultiClass
from ._datastructs import SemanticMapOverlapping, SemanticLabelmap
from ._datastructs import InstanceMapOverlapping, InstanceLabelmap
from ._datastructs import raise_if_not_none_or_iterable_of_annotations

from ._creation import create_model, create_config
from ._creation import create_from_config
from ._creation import templates, add_module

from ._io import save_model, load_model
from ._io import save_config, load_config
from ._io import save_checkpoint, load_checkpoint
from ._io import to_storable_dict, from_storable_dict

# Finally import extension after completed initialization of tacotree
import tacotree_lab as lab


__version__ = '1.0.0'
__author__ = 'Matthias Nadig'
