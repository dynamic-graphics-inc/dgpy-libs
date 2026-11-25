<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy-banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# aiopen

[![Wheel](https://img.shields.io/pypi/wheel/aiopen.svg)](https://img.shields.io/pypi/wheel/aiopen.svg) [![Version](https://img.shields.io/pypi/v/aiopen.svg)](https://img.shields.io/pypi/v/aiopen.svg) [![py_versions](https://img.shields.io/pypi/pyversions/aiopen.svg)](https://img.shields.io/pypi/pyversions/aiopen.svg) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**Install:** `pip install aiopen`

> **Breaking change (v0.9.0):** the `aiopen` module is no longer callable.
> Replace `import aiopen; aiopen(...)` with `from aiopen import aiopen; aiopen(...)`.

Async-open

**Why not use aiofiles?**

- Wanted more type annotations
- aiofiles uses ye ole `@coroutine` decorator -- aiopen uses python3.6+ `async/await`

(Big shouts out to the aiofiles people, aiopen is entirely based off of aiofiles)

## Usage

Just import it!

```python
from aiopen import aiopen

async with aiopen("afile.txt", "w") as f:
    await f.write("some text!")

async with aiopen("afile.txt", "r") as f:
    content = await f.read()
    print(content)
```
