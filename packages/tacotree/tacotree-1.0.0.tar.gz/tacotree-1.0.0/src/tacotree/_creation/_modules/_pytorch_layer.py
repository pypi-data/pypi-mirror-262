# Copyright (C) 2024 Matthias Nadig

# DO NOT REMOVE!!!
# Importing torch is required for eval function!
import torch
# DO NOT REMOVE!!!

from ._base import Module


class PyTorchLayer(Module):
    """
    Helper to extract data from batch type, when using inbuilt torch modules
    """

    def __init__(self, name, **params):
        super().__init__()
        layer_class = safe_instantiation_of_layer(name_layer=name)
        self._processor = layer_class(**params)

    def _forward(self, *args):
        n_inputs = len(args)
        if n_inputs == 1:
            # Unpack the batch
            batch = args[0]
            x, annotations, limits = batch.data(), batch.annotations(), batch.limits()

            # Run PyTorch module
            x = self._processor(x)

            # Caveat!
            # Bounding boxes and similar annotations might be inaccurate after this layer in the current implementation.
            # This is due to PyTorch modules that change the shape of the data. For now, we therefore do not
            # forward the annotations here.
            out = self._as_batch(data=x, annotations=None, limits=None)
        else:
            str_e = f'Currently only single inputs are allowed to be given to PyTorch modules'
            raise ValueError(str_e)

        return out


def safe_instantiation_of_layer(name_layer):
    str_reference = f'torch.nn.{name_layer}'
    return _safe_instantiation(str_reference)


def _safe_instantiation(str_reference):
    """
    CAVEAT!
    This function uses eval(). Therefore, it first checks the input for alphanumeric
    characters to ensure, no malicious code is executed.
    """

    # Throw if module name
    #   - contains non-alphanumeric characters (except for "." and "_") or
    #   - does not start with "torch."
    chars_check = str_reference.replace('.', '').replace('_', '')
    is_alphanumeric = chars_check.isascii() and chars_check.isalnum()
    is_torch_attribute = str_reference.startswith('torch.')
    if not is_alphanumeric or not is_torch_attribute:
        str_e = f'Got input that is non-alphanumeric or does not reference an attribute of torch: "{str_reference}"'
        raise ValueError(str_e)

    # Get the required attribute
    attr = eval(str_reference)

    return attr
