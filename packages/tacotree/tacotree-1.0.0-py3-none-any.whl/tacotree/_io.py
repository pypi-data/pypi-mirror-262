# Copyright (C) 2024 Matthias Nadig

import os
import json

import torch

from ._creation import create_from_config
from ._creation import Config
from ._creation import Model


_FILETYPE_MODEL = 'ttmodel'
_FILETYPE_CONFIG = 'ttconfig'
_FILETYPE_CHECKPOINT = 'ttcheckpoint'


def to_storable_dict(model):
    obj = dict(
        config=model.get_config().to_json_compatible(),
        state_dict=model.state_dict(),
    )
    return obj


def from_storable_dict(obj, debug=False):
    config = Config.from_json_compatible(obj['config'])
    state_dict = obj['state_dict']
    model = create_from_config(config=config, debug=debug)
    model.load_state_dict(state_dict)
    return model


def save_model(filename, model, overwrite=False, makedirs=False):
    filename = _add_appendix_model(filename)

    if os.path.isfile(filename) and not overwrite:
        raise FileExistsError(f'"{filename}"')
    if makedirs:
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)

    obj = to_storable_dict(model)
    torch.save(obj, filename)


def load_model(filename, debug=False):
    filename = _add_appendix_model(filename)

    map_location = torch.device('cpu')
    obj = torch.load(filename, map_location=map_location)
    model = from_storable_dict(obj, debug=debug)

    return model


def save_config(filename, obj, overwrite=False, makedirs=False):
    filename = _add_appendix_config(filename)

    if os.path.isfile(filename) and not overwrite:
        raise FileExistsError(f'"{filename}"')
    if makedirs:
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)

    if isinstance(obj, Model):
        # Read config of given model
        obj = obj.config.to_json_compatible()
    elif isinstance(obj, Config):
        # Config is given directly
        obj = obj.to_json_compatible()
    else:
        raise TypeError(f'Expected object of type Model or Config, got {type(obj)}')

    with open(filename, 'w') as f:
        json.dump(obj, f)


def load_config(filename):
    filename = _add_appendix_config(filename)

    with open(filename, 'r') as f:
        config = json.load(f)
    config = Config.from_json_compatible(config)

    return config


def save_checkpoint(filename, model, metadata, overwrite=False, makedirs=False):
    filename = _add_appendix_checkpoint(filename)

    if os.path.isfile(filename) and not overwrite:
        raise FileExistsError(f'"{filename}"')
    if makedirs:
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)

    obj = dict(
        model=to_storable_dict(model),
        metadata=metadata,
    )
    torch.save(obj, filename)


def load_checkpoint(filename, debug=False):
    filename = _add_appendix_checkpoint(filename)

    map_location = torch.device('cpu')
    obj = torch.load(filename, map_location=map_location)
    model = from_storable_dict(obj['model'], debug=debug)
    metadata = obj['metadata']

    return model, metadata


def _add_appendix_model(filename):
    return _add_appendix(filename, _FILETYPE_MODEL)


def _add_appendix_config(filename):
    return _add_appendix(filename, _FILETYPE_CONFIG)


def _add_appendix_checkpoint(filename):
    return _add_appendix(filename, _FILETYPE_CHECKPOINT)


def _add_appendix(filename, filetype):
    appendix = '.' + filetype
    return filename + appendix if not filename.endswith(appendix) else filename
