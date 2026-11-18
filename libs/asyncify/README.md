<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner_dark.svg?raw=true">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</picture>
</a>

# asyncify

[![Wheel](https://img.shields.io/pypi/wheel/asyncify.svg)](https://img.shields.io/pypi/wheel/asyncify.svg)
[![Version](https://img.shields.io/pypi/v/asyncify.svg)](https://img.shields.io/pypi/v/asyncify.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/asyncify.svg)](https://img.shields.io/pypi/pyversions/asyncify.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**TLDR:** Sync 2 Async decorator

**Install:** `pip install asyncify`

> **Breaking change (v0.13.0):** the `asyncify` module is no longer callable. Replace `import asyncify; @asyncify` with `from asyncify import asyncify; @asyncify`.

**Usage:**

```python
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
