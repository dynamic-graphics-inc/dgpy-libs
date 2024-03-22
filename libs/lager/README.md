<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# lager :beer:

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
from lager import LOG, lager, LAGER, log, logger  # All the same object

LOG.info("info")
```

    2022-07-21 08:38:20.263 | INFO     | __main__:<cell line: 3>:3 - info
