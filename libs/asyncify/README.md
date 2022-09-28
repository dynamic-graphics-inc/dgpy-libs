<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# asyncify

[![Wheel](https://img.shields.io/pypi/wheel/asyncify.svg)](https://img.shields.io/pypi/wheel/asyncify.svg)
[![Version](https://img.shields.io/pypi/v/asyncify.svg)](https://img.shields.io/pypi/v/asyncify.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/asyncify.svg)](https://img.shields.io/pypi/pyversions/asyncify.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**TLDR:** Sync 2 Async decorator

**Install:** `pip install asyncify`

**Usage:**

```python
import asyncify

# OR
from asyncify import asyncify
from asyncify import run  # asyncio.run polyfill for python36


def add(a, b):
    return a + b


assert add(1, 2) == 3


@asyncify
def add_async(a, b):
    return a + b


res = await add_async(1, 2)
assert res == 3
```
