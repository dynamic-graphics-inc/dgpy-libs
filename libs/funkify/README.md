<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# funkify

[![Wheel](https://img.shields.io/pypi/wheel/funkify.svg)](https://img.shields.io/pypi/wheel/funkify.svg)
[![Version](https://img.shields.io/pypi/v/funkify.svg)](https://img.shields.io/pypi/v/funkify.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/funkify.svg)](https://img.shields.io/pypi/pyversions/funkify.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**Install:** `pip install funkify`

Make a module/package/script callable.

## Usage:

### 1) Write a file called `a_module.py` with some function and decorate said function with funkify

```python
import funkify

@funkify
def some_funk_name_doesnt_matter():
	return 'howdy'
```

### 2) Import a_module and call it like you would a function!

```python
import a_module
a_module.some_funk_name_doesnt_matter_what_it_is()  # returns 'howdy'
a_module()  # ALSO returns 'howdy'
```
