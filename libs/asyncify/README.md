<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" height="120"/>
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


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-9f3a53cb7576> in <module>
    ----> 1 import asyncify
          2 # OR
          3 from asyncify import asyncify
          4 from asyncify import run  # asyncio.run polyfill for python36
          5 


    /mnt/d/dgpy-dev/dgpy-libs/libs/asyncify/asyncify/__init__.py in <module>
          4 from asyncify.core import asyncify, run
          5 
    ----> 6 from funkify import funkify
          7 
          8 


    ModuleNotFoundError: No module named 'funkify'

