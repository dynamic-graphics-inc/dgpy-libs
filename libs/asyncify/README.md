<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# asyncify

[![Wheel](https://img.shields.io/pypi/wheel/asyncify.svg)](https://img.shields.io/pypi/wheel/asyncify.svg)
[![Version](https://img.shields.io/pypi/v/asyncify.svg)](https://img.shields.io/pypi/v/asyncify.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/asyncify.svg)](https://img.shields.io/pypi/pyversions/asyncify.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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
