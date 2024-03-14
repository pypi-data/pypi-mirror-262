# Copyright (C) 2024 Matthias Nadig

from ._pytorch_layer import PyTorchLayer, safe_instantiation_of_layer
from . import templates
from .templates import Input, Output
from .templates import SequentialSingleInput, SequentialMultipleInputs


_MODULE_CONSTRUCTORS = {
    # Shape
    'Flatten': templates.Flatten,
    'Vectorize': templates.Vectorize,
    'Reshape': templates.Reshape,
    'View': templates.View,
    'Transpose': templates.Transpose,
    'SwapAxes': templates.SwapAxes,
    'Concat': templates.Concat,
    'Stack': templates.Stack,
    'Squeeze': templates.Squeeze,
    'Unsqueeze': templates.Unsqueeze,

    # Math
    'Add': templates.Add,

    # Global pooling
    'GlobalAverage': templates.GlobalAverage,
    'GlobalMax': templates.GlobalMax,

    # Padding
    'CircularPad1d': templates.CircularPad1d,
    'CircularPad': templates.CircularPad,

    # Others
    'Argmax': templates.Argmax,
    'DebugBreakpoint': templates.DebugBreakpoint,
    'PassThrough': templates.PassThrough,
    'Lambda': templates.Lambda,
    'SelectFromTuple': templates.SelectFromTuple,
    'TTModel': templates.TTModel,
}

# Special sequential modules
# Dictionary that provides the constructor for a sequential for some modules.
# Such constructors can be given by the user if a set of custom modules is more
# efficient with a special way of handling sequential execution.
# Example: Custom pipeline class that should be used with some custom modules for
# preprocessing or augmentation.
_MODULES_WITH_SPECIAL_SEQUENTIALS = {}


def create_sequence(modules, debug, has_multiple_inputs):
    if len(modules) == 1:
        # Sequence of a single module (does not require a sequential wrapper)
        module_info = modules[0]
        # (name, params) = module_info  # params can sometimes not be specified
        seq = _get_module(*module_info, debug=debug)
    else:
        # Sequence has multiple modules, choose the appropriate sequential wrapper
        module_names = [m[0] for m in modules]
        constructor_sequential = _get_sequential_constructor(module_names=module_names,
                                                             has_multiple_inputs=has_multiple_inputs)
        modules_built = [_get_module(*module_info, debug=debug) for module_info in modules]
        seq = constructor_sequential().create(modules=modules_built, debug=debug)

    return seq


def add_module(name, constructor, sequential_constructor=None):
    # Use shorter names for variables, otherwise code becomes too much text
    c = constructor
    sc = sequential_constructor
    del constructor, sequential_constructor

    # Check input types
    if not isinstance(name, str):
        str_e = f'Name must be a string, got {type(name)}'
        raise TypeError(str_e)
    elif name in _MODULE_CONSTRUCTORS:
        str_e = f'A module type with name "{name}" already exists'
        raise ValueError(str_e)
    if not issubclass(c, templates.Module):
        str_e = f'Constructor must be of Module type, got {type(c)}'
        raise TypeError(str_e)
    if sc is not None:
        is_valid_sequential = \
            issubclass(sc, templates.SequentialBase) or \
            (hasattr(sc, '__iter__') and all([issubclass(item, templates.SequentialBase) for item in sc]))
        if not is_valid_sequential:
            str_e = \
                f'Sequential constructor must be None, SequentialBase or iterable of SequentialBase, got {type(sc)}'
            raise TypeError(str_e)
        elif name in _MODULES_WITH_SPECIAL_SEQUENTIALS:
            str_e = f'Sequential constructor for module already exists'
            raise RuntimeError(str_e)

    # Add module
    _MODULE_CONSTRUCTORS[name] = c

    # Add special sequential constructor, if given
    if sc is not None:
        _MODULES_WITH_SPECIAL_SEQUENTIALS[name] = sc


def _get_module(name, params=None, debug=False):
    if name == 'Input':
        module_class = Input
    elif name == 'Output':
        module_class = Output
    elif name in _MODULE_CONSTRUCTORS:
        module_class = _MODULE_CONSTRUCTORS[name]
    else:
        # Note:
        # If a module name is not available, this else-statement will be entered but the error
        # will be thrown below in module_class(**params).
        module_class = _get_pytorch_wrapper(name=name)

    params = dict() if params is None else params

    try:
        module = module_class(**params)
        module = module.set_debug(debug=debug)
    except AttributeError:  # as e:
        names_available = list(_MODULE_CONSTRUCTORS.keys()) + ['PyTorch modules in torch.nn']
        n_available = len(names_available)
        str_error = (
            f'Module not found\n\nAvailable modules:' + ('\n\t* {}' * n_available).format(*names_available) +
            f'\n\nModule "{name}" not found. For a list of available modules, see above.'
        )
        raise ValueError(str_error)

    return module


def _get_sequential_constructor(module_names, has_multiple_inputs):
    # Get special constructors for each module
    special_constructors = [
        _MODULES_WITH_SPECIAL_SEQUENTIALS[name] if name in _MODULES_WITH_SPECIAL_SEQUENTIALS else None
        for name in module_names
    ]
    special_constructors_found = []
    for special_constructor in special_constructors:
        if not hasattr(special_constructor, '__iter__'):
            special_constructor = [special_constructor]
        for special_constructor_current in special_constructor:
            if special_constructor_current not in special_constructors_found:
                special_constructors_found.append(special_constructor_current)

    # Check if all modules are eligible for one and the same special constructor
    special_constructors_valid = []
    for special_constructor in special_constructors_found:
        if all([
            special_constructor == c_check or
            (hasattr(c_check, '__iter__') and special_constructor in c_check)
            for c_check in special_constructors
        ]):
            special_constructors_valid.append(special_constructor)

    # Pick the first one (this will be None, if no special constructors are registered)
    if len(special_constructors_valid) > 0:
        special_constructor_used = special_constructors_valid[0]
    else:
        special_constructor_used = None

    # Choose constructor for sequential modules
    if special_constructor_used is None:
        # Use the default one
        if has_multiple_inputs:
            constructor_sequential = SequentialMultipleInputs
        else:
            constructor_sequential = SequentialSingleInput
    else:
        # Use the chosen special constructor
        constructor_sequential = special_constructor_used

    return constructor_sequential


def _get_pytorch_wrapper(name):
    """ Returns a callable that initializes a PyTorch layer """
    def wrap_pytorch_layer(**params):
        return PyTorchLayer(name=name, **params)
    return wrap_pytorch_layer
