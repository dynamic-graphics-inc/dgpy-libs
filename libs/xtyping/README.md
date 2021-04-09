<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>


# xtyping

[![Wheel](https://img.shields.io/pypi/wheel/xtyping.svg)](https://img.shields.io/pypi/wheel/xtyping.svg)
[![Version](https://img.shields.io/pypi/v/xtyping.svg)](https://img.shields.io/pypi/v/xtyping.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/xtyping.svg)](https://img.shields.io/pypi/pyversions/xtyping.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install xtyping`

___

xtyping (short for extended typing) is a collection of common python type annotation aliases. Most common members of `typing` are also importable from `xtyping`.

If you want to 'steal' this, you can copy the module `xtyping._xtyping` and never look back; alternatively you could help expand/correct this package you could send me that PR!'

NOTE: This package is largely auto generated so have a grain of salt with your xtyping   

```python
import xtyping as xt
# or
from xtyping import xt

xt.DictAny # equiv to `Dict[Any, Any]`
xt.Number # equiv to `Union[int, float]`
# etc
```

## Why not use `typing_extensions`?

Too many letters to type and 'xtyping' is a better package name (tho `typing_extensions` is an excellent package).

## TODO:

 - Numpy/pandas integration
 - Pydantic extension/integration/buzzword
 - Figure out how to test this package?
 - Steal `typing_extensions` implementation o ye ole `TypedDict`

