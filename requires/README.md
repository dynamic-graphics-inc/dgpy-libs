# funkify

<img src="https://github.com/dynamic-graphics-inc/dgimages/blob/master/dgpy/dgpy_logo.svg?raw=true" alt="drawing" width="120"/> **Dynamic Graphics Python**

[![Wheel](https://img.shields.io/pypi/wheel/funkify.svg)](https://img.shields.io/pypi/wheel/funkify.svg)
[![Version](https://img.shields.io/pypi/v/funkify.svg)](https://img.shields.io/pypi/v/funkify.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/funkify.svg)](https://img.shields.io/pypi/pyversions/funkify.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install funkify`

___

## Who? What? Where? When? Why?

**WHO???** jesse @ dgi

**WHAT???** (tiny) Lib/package that lets ya make a module callable

**WHERE???** Dynamic Graphics Inc

**WHEN???** 9 => 5 on workdays

**WHY???** Two reasons: **1)** Why not? **2)** It is pretty cool and I have always wanted something like this for tiny modules/packages centered around a singular function

___

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
