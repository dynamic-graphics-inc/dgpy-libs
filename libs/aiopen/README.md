<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# aiopen

[![Wheel](https://img.shields.io/pypi/wheel/aiopen.svg)](https://img.shields.io/pypi/wheel/aiopen.svg)
[![Version](https://img.shields.io/pypi/v/aiopen.svg)](https://img.shields.io/pypi/v/aiopen.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/aiopen.svg)](https://img.shields.io/pypi/pyversions/aiopen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install aiopen`

Async-open

**Why not use aiofiles?**

- Wanted more type annotations
- aiofiles uses ye ole `@coroutine` decorator -- aiopen uses python3.6+ `async/await`
- aiopen is a callable module, so you can do:
  - `import aiopen`
  - `async with aiopen('afile.txt', 'w') as f: await f.write('some text!')`
  - `async with aiopen('afile.txt', 'r') as f: content = await f.read()`

(Big shouts out to the aiofiles people, aiopen is entirely based off of aiofiles)

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
