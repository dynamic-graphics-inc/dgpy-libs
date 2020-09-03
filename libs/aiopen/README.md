# aiopen

<img src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" width="320"/>

[![Wheel](https://img.shields.io/pypi/wheel/aiopen.svg)](https://img.shields.io/pypi/wheel/aiopen.svg)
[![Version](https://img.shields.io/pypi/v/aiopen.svg)](https://img.shields.io/pypi/v/aiopen.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/aiopen.svg)](https://img.shields.io/pypi/pyversions/aiopen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install aiopen`

___

## Who? What? Where? When? Why?

**WHO???** The dgpy team and the people who wrote aiofiles which is the basis for aiopen

**WHAT???** Asyncio open for python36 and up

**WHERE???** Dynamic Graphics Inc in this repo

**WHEN???** 9 => 5 on workdays

**WHY???** Three reasons: **1)** I have used the pip package aiofiles (`pip install aiofiles`) quite a bit, and I wanted a more type-annotation-friendly version of aiofiles **2)** aiopen uses funkify (`pip install funkify`) so the imported is callable as `aiopen` (see examples below) **3)** Async file io with out ye ole `@coroutine` decorator; Aiofiles supportes python3.5 which is dark-ages async-python.

(Big shouts out to the aiofiles people, aiopen is entirely based off of aiofiles)


___

## Usage:

Just import it! The module is also callable!


```python
import aiopen

async with aiopen('afile.txt', 'w') as f:
    await f.write('some text!')

async with aiopen('afile.txt', 'r') as f:
    content = await f.read()
    print(content)

```

    some text!

