# -*- coding: utf-8 -*-
"""Pre-fab requirements"""
from requires import Requirement


__all__ = [
    'requires_boto3',
    'requires_toml',
    'requires_imageio',
    'require_msgpack',
    'requires_ipython',
    'requires_ruamel_yaml',
]

require_msgpack = Requirement(
    _import='msgpack',
    pip='msgpack',
    conda='msgpack-python',
    conda_forge='msgpack-python',
)
requires_toml = Requirement(_import='toml', pip=True, conda=True, conda_forge=True)
requires_ruamel_yaml = Requirement(
    _import='ruamel.yaml', pip='ruamel.yaml', conda=False, conda_forge='ruamel_yaml'
)
requires_ipython = Requirement(
    _import='IPython', pip='ipython', conda='ipython', conda_forge='ipython'
)
requires_imageio = Requirement(
    _import='imageio', pip=True, conda=True, conda_forge=True
)
requires_boto3 = Requirement(_import='boto3', pip=True, conda=True, conda_forge=True)
