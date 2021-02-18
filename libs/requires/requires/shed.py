# -*- coding: utf-8 -*-
"""Pre-fab requirements"""
from requires import Requirement


__all__ = [
    'requires_boto3',
    'requires_toml',
    'requires_imageio',
    'requires_msgpack',
    'requires_ipython',
    'requires_ruamel_yaml',
    'requires_orjson',
    'requires_rapidjson',
    'requires_python_rapidjson',
    'requires_numpy',
    'requires_pandas',
    'requires_scipy',
    'requires_httpx',
    'requires_h5py',
    'requires_xarray',
    'requires_pydantic',
    'requires_zmq',
]

requires_numpy = Requirement(
    _import='numpy',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_pandas = Requirement(
    _import='pandas',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_scipy = Requirement(
    _import='scipy',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_h5py = Requirement(
    _import='h5py',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_xarray = Requirement(
    _import='xarray',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_msgpack = Requirement(
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
requires_orjson = Requirement(
    _import='orjson',
    pip=True,
    conda=False,
    conda_forge=True,
)
requires_rapidjson = Requirement(
    _import='rapidjson',
    pip='python-rapidjson',
    conda='python-rapidjson',
    conda_forge='python-rapidjson',
)
requires_python_rapidjson = requires_rapidjson  # Alias for python rapidjson
requires_pydantic = Requirement(
    _import='pydantic',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_httpx = Requirement(
    _import='httpx',
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_zmq = Requirement(
    _import='zmq',
    pip='pyzmq',
    conda='pyzmq',
    conda_forge='pyzmq',
)
