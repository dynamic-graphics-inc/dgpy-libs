<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" height="120"/>
</a>

# Lager :beer:


[![Wheel](https://img.shields.io/pypi/wheel/lager.svg)](https://img.shields.io/pypi/wheel/lager.svg)
[![Version](https://img.shields.io/pypi/v/lager.svg)](https://img.shields.io/pypi/v/lager.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/lager.svg)](https://img.shields.io/pypi/pyversions/lager.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install lager`

Logging library based off of loguru (`pip install loguru`).

**Why not just use loguru?**

 - Lager is a better pun
 - Lager is really a utility pack for loguru

BTW: Loguru is an amazing lib. Check it out: https://github.com/Delgan/loguru

## Usage:



```python
from lager import LOG
LOG.info('info')
LOG.i('info')
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-36faeb76e3af> in <module>
    ----> 1 from lager import LOG
          2 LOG.info('info')
          3 LOG.i('info')


    /mnt/d/dgpy-dev/dgpy-libs/libs/lager/lager/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """Python lager brewed by a loguru"""
    ----> 3 from lager import logging
          4 from lager._meta import __version__
          5 from lager.const import LAGER_PORT, LOGURU_DEFAULT_FMT, TORNADO_FMT


    /mnt/d/dgpy-dev/dgpy-libs/libs/lager/lager/logging.py in <module>
          5 from typing import Any, Dict, List
          6 
    ----> 7 from lager.core import LOG, loglevel
          8 
          9 


    /mnt/d/dgpy-dev/dgpy-libs/libs/lager/lager/core.py in <module>
          9 from typing import Any, Callable, Dict, Optional, TypeVar, Union
         10 
    ---> 11 from loguru import _defaults
         12 from loguru._handler import Handler
         13 from loguru._logger import Core as _Core, Logger as _Logger


    ModuleNotFoundError: No module named 'loguru'

