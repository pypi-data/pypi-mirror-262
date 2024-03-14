# Copyright (C) 2024 Matthias Nadig

import io
import base64
import numpy as np

from ._model import Model


class Config:
    # Version for compatibility within this toolbox
    VERSION_MAX = 4

    def __init__(self, sequences, workflow, groups=None, version=None):
        super().__init__()
        self.version = self.VERSION_MAX if version is None else version
        self.workflow = workflow

        # self.groups = {'all': [i for i in range(len(self.workflow))]}
        if groups is not None:
            if 'all' in groups:
                str_e = f'Workflow groups have been specified by user and contain invalid group name "all": {groups}'
                raise ValueError(str_e)
            # self.groups = dict(**self.groups, **groups)
            self.groups = groups
        else:
            self.groups = dict()

        sequences_set = dict()
        for seq_name, seq in sequences.items():
            sequences_set[seq_name] = []
            for module in seq:
                if isinstance(module, Model):
                    module = (
                        'TTModel',
                        dict(
                            order_inputs=module.get_input_names(),
                            order_outputs=module.get_output_names(),
                            config=module.get_config(),
                            state_dict=module.state_dict(),
                        )
                    )
                elif module[0] == 'Source':
                    # How to work with Array data? --> axis modification etc. currently designed to work on samples
                    raise NotImplementedError('Implement Source module in model first')
                    # Make sure that data of source is JSON-serializable in config
                    data = module[1]['data']
                    data = np.asarray(data)
                    dtype_source = data.dtype
                    # if not np.issubdtype(dtype_source, np.number):  # this would allow complex numbers
                    if not (np.issubdtype(dtype_source, np.integer) or np.issubdtype(dtype_source, np.floating)):
                        str_e = f'Data type {dtype_source} not allowed for Source module'
                        raise ValueError(str_e)
                    with io.BytesIO() as sink:
                        np.save(sink, data)
                        bytes_data = sink.getvalue()
                    str_data = base64.b64encode(bytes_data).decode()
                    module = (
                        module[0],
                        dict(data=str_data)
                    )
                else:
                    pass
                sequences_set[seq_name].append(module)
        self.sequences = sequences_set

    @staticmethod
    def from_json_compatible(obj):
        # Ignore version 1 and 2
        version = 1 if 'version' not in obj else obj['version']
        if version == 3:
            if 'groups' in obj:
                str_e = f'Groups not expected to be given for model of version {version} (obj = {obj})'
                raise RuntimeError(str_e)
            obj['groups'] = None
        else:
            if version != Config.VERSION_MAX:
                raise RuntimeError(f'Version {version} not compatible (accepted versions: {Config.VERSION_MAX})')
        return Config(sequences=obj['sequences'], workflow=obj['workflow'], groups=obj['groups'], version=version)

    def to_json_compatible(self):
        obj = dict(
            version=self.version,
            sequences=self.sequences,
            workflow=self.workflow,
            groups=self.groups,
        )
        return obj
