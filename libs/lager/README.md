# Lager :beer:

<img src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" width="320"/>

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

    2020-11-24 11:09:32.074 | INFO     | __main__:<module>:2 - info



    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-1-36faeb76e3af> in <module>
          1 from lager import LOG
          2 LOG.info('info')
    ----> 3 LOG.i('info')
    

    AttributeError: 'Logger' object has no attribute 'i'

