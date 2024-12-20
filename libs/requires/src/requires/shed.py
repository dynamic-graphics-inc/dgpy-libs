# -*- coding: utf-8 -*-
"""Pre-fab requirements"""

from __future__ import annotations

from requires import Requirement

__all__ = (
    "requires_anyio",
    "requires_attrs",
    "requires_black",
    "requires_boto3",
    "requires_botocore",
    "requires_bottleneck",
    "requires_bottleneck_as_bn",
    "requires_cattrs",
    "requires_click",
    "requires_h5py",
    "requires_httpx",
    "requires_hypothesis",
    "requires_imageio",
    "requires_imageio_as_iio",
    "requires_ipython",
    "requires_msgpack",
    "requires_nox",
    "requires_numba",
    "requires_numba_as_nb",
    "requires_numpy",
    "requires_numpy_as_np",
    "requires_opencv",
    "requires_orjson",
    "requires_pandas",
    "requires_pandas_as_pd",
    "requires_polars",
    "requires_polars_as_pl",
    "requires_pydantic",
    "requires_pytest",
    "requires_pytest_asyncio",
    "requires_pytest_cov",
    "requires_pytest_xdist",
    "requires_python_rapidjson",
    "requires_rapidjson",
    "requires_rich",
    "requires_ruamel_yaml",
    "requires_ry",
    "requires_scipy",
    "requires_toml",
    "requires_tomli",
    "requires_tox",
    "requires_typing_extensions",
    "requires_typing_extensions_as_te",
    "requires_typing_extensions_as_tx",
    "requires_ujson",
    "requires_xarray",
    "requires_xarray_as_xr",
    "requires_xdoctest",
    "requires_yaml",
    "requires_zmq",
)

# NUMPY & PANDAS & SCIPY, oh my!
requires_numpy = Requirement(
    _import="numpy",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_numpy_as_np = Requirement(
    _import="numpy",
    _as="np",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_h5py = Requirement(
    _import="h5py",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_pandas = Requirement(
    _import="pandas",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_pandas_as_pd = Requirement(
    _import="pandas",
    _as="pd",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_scipy = Requirement(
    _import="scipy",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_xarray = Requirement(
    _import="xarray",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_xarray_as_xr = Requirement(
    _import="xarray",
    _as="xr",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_polars = Requirement(
    _import="polars",
    pip=True,
    conda=False,
    conda_forge=True,
)
requires_polars_as_pl = Requirement(
    _import="polars",
    _as="pl",
    pip=True,
    conda=False,
    conda_forge=True,
)
requires_numba = Requirement(
    _import="numba",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_numba_as_nb = Requirement(
    _import="numba",
    _as="nb",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_bottleneck = Requirement(
    _import="bottleneck",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_bottleneck_as_bn = Requirement(
    _import="bottleneck",
    _as="bn",
    pip=True,
    conda=True,
    conda_forge=True,
)

# OPENCV
requires_opencv = Requirement(
    _import="cv2",
    pip="opencv-python",
    conda="opencv",
    conda_forge="opencv",
)

# BLACK
requires_black = Requirement(
    _import="black",
    pip=True,
    conda=True,
    conda_forge=True,
)

# IPYTHON
requires_ipython = Requirement(
    _import="IPython", pip="ipython", conda="ipython", conda_forge="ipython"
)

# IMAGEIO
requires_imageio = Requirement(
    _import="imageio", pip=True, conda=True, conda_forge=True
)
requires_imageio_as_iio = Requirement(
    _import="imageio.v3", _as="iio", pip=True, conda=True, conda_forge=True
)

# AWS
requires_boto3 = Requirement(_import="boto3", pip=True, conda=True, conda_forge=True)
requires_botocore = Requirement(
    _import="botocore", pip=True, conda=True, conda_forge=True
)

# PYDANTIC
requires_pydantic = Requirement(
    _import="pydantic",
    pip=True,
    conda=True,
    conda_forge=True,
)

# ATTRS
requires_attrs = Requirement(
    _import="attrs",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_cattrs = Requirement(
    _import="cattrs",
    pip=True,
    conda=True,
    conda_forge=True,
)

# AIO
requires_anyio = Requirement(
    _import="anyio",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_httpx = Requirement(
    _import="httpx",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_zmq = Requirement(
    _import="zmq",
    pip="pyzmq",
    conda="pyzmq",
    conda_forge="pyzmq",
)

# JSON
requires_orjson = Requirement(
    _import="orjson",
    pip=True,
    conda=False,
    conda_forge=True,
)
requires_rapidjson = Requirement(
    _import="rapidjson",
    pip="python-rapidjson",
    conda="python-rapidjson",
    conda_forge="python-rapidjson",
)
requires_python_rapidjson = requires_rapidjson  # Alias for python rapidjson
requires_ujson = Requirement(
    _import="ujson",
    pip=True,
    conda=True,
    conda_forge=True,
)

# MSGPACK
requires_msgpack = Requirement(
    _import="msgpack",
    pip="msgpack",
    conda="msgpack-python",
    conda_forge="msgpack-python",
)

# TOML
requires_toml = Requirement(_import="toml", pip=True, conda=True, conda_forge=True)
requires_tomli = Requirement(_import="tomli", pip=True, conda=True, conda_forge=True)

# YAML
requires_yaml = Requirement(
    _import="yaml", pip="PyYAML", conda="PyYAML", conda_forge="PyYAML"
)
requires_ruamel_yaml = Requirement(
    _import="ruamel.yaml",
    pip="ruamel.yaml",
    conda=False,
    conda_forge="ruamel_yaml",
)

# RICH
requires_rich = Requirement(_import="rich", pip=True, conda=True, conda_forge=True)

# CLICK
requires_click = Requirement(_import="click", pip=True, conda=True, conda_forge=True)

# TESTING
requires_hypothesis = Requirement(
    _import="hypothesis", pip=True, conda=True, conda_forge=True
)
requires_pytest = Requirement(
    _import="pytest",
    pip=True,
    conda=True,
    conda_forge=True,
)
requires_pytest_asyncio = Requirement(
    _import="pytest_asyncio",
    pip="pytest-asyncio",
    conda="pytest-asyncio",
    conda_forge="pytest-asyncio",
)
requires_pytest_cov = Requirement(
    _import="pytest_cov",
    pip="pytest-cov",
    conda="pytest-cov",
    conda_forge="pytest-cov",
)
requires_pytest_xdist = Requirement(
    _import="xdist",
    pip="pytest-xdist",
    conda="pytest-xdist",
    conda_forge="pytest-xdist",
)
requires_xdoctest = Requirement(
    _import="xdoctest",
    pip=True,
    conda=False,
    conda_forge=True,
)

# TYPING
requires_typing_extensions = Requirement(
    _import="typing_extensions", pip=True, conda=True, conda_forge=True
)
requires_typing_extensions_as_te = Requirement(
    _import="typing_extensions", _as="te", pip=True, conda=True, conda_forge=True
)
requires_typing_extensions_as_tx = Requirement(
    _import="typing_extensions", _as="tx", pip=True, conda=True, conda_forge=True
)

# NOX
requires_nox = Requirement(_import="nox", pip=True, conda=True, conda_forge=True)
# TOX
requires_tox = Requirement(_import="tox", pip=True, conda=True, conda_forge=True)

# RY
requires_ry = Requirement(_import="ry", pip=True, conda=False, conda_forge=False)
