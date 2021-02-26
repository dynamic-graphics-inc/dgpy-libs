<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" height="120"/>
</a>

# dgpy-libs

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dynamic-graphics-inc/dgpy-libs/master?filepath=README.ipynb)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Dynamic Graphics python libraries, home of:

 - Callable modules and packages
 - Recursive list/gen comprehensions
 - Nutty decorators
 - Secret agent JSON Bourne
 - The best package names around
 - Notebooks with funky python
 - Dynamic imports

## Libs

```
libs
├── aiopen
├── asyncify
├── funkify
├── h5
├── jsonbourne
├── lager
├── requires
└── xtyping
```


### [aiopen](./libs/aiopen/README.md) ~ `pip install aiopen` ~ [![Wheel](https://img.shields.io/pypi/wheel/aiopen.svg)](https://img.shields.io/pypi/wheel/aiopen.svg) [![Version](https://img.shields.io/pypi/v/aiopen.svg)](https://img.shields.io/pypi/v/aiopen.svg) [![py_versions](https://img.shields.io/pypi/pyversions/aiopen.svg)](https://img.shields.io/pypi/pyversions/aiopen.svg)

### [asyncify](./libs/asyncify/README.md) ~ `pip install asyncify` ~ [![Wheel](https://img.shields.io/pypi/wheel/asyncify.svg)](https://img.shields.io/pypi/wheel/asyncify.svg) [![Version](https://img.shields.io/pypi/v/asyncify.svg)](https://img.shields.io/pypi/v/asyncify.svg) [![py_versions](https://img.shields.io/pypi/pyversions/asyncify.svg)](https://img.shields.io/pypi/pyversions/asyncify.svg)

### [funkify](./libs/funkify/README.md) ~ `pip install funkify` ~ [![Wheel](https://img.shields.io/pypi/wheel/funkify.svg)](https://img.shields.io/pypi/wheel/funkify.svg) [![Version](https://img.shields.io/pypi/v/funkify.svg)](https://img.shields.io/pypi/v/funkify.svg) [![py_versions](https://img.shields.io/pypi/pyversions/funkify.svg)](https://img.shields.io/pypi/pyversions/funkify.svg)

### [h5](./libs/h5/README.md) ~ `pip install h5` ~ [![Wheel](https://img.shields.io/pypi/wheel/h5.svg)](https://img.shields.io/pypi/wheel/h5.svg) [![Version](https://img.shields.io/pypi/v/h5.svg)](https://img.shields.io/pypi/v/h5.svg) [![py_versions](https://img.shields.io/pypi/pyversions/h5.svg)](https://img.shields.io/pypi/pyversions/h5.svg)

### [jsonbourne](./libs/jsonbourne/README.md) ~ `pip install jsonbourne` ~ [![Wheel](https://img.shields.io/pypi/wheel/jsonbourne.svg)](https://img.shields.io/pypi/wheel/jsonbourne.svg) [![Version](https://img.shields.io/pypi/v/jsonbourne.svg)](https://img.shields.io/pypi/v/jsonbourne.svg) [![py_versions](https://img.shields.io/pypi/pyversions/jsonbourne.svg)](https://img.shields.io/pypi/pyversions/jsonbourne.svg)

### [lager](./libs/lager/README.md) ~ `pip install lager` ~ [![Wheel](https://img.shields.io/pypi/wheel/lager.svg)](https://img.shields.io/pypi/wheel/lager.svg) [![Version](https://img.shields.io/pypi/v/lager.svg)](https://img.shields.io/pypi/v/lager.svg) [![py_versions](https://img.shields.io/pypi/pyversions/lager.svg)](https://img.shields.io/pypi/pyversions/lager.svg)

### [requires](./libs/requires/README.md) ~ `pip install requires` ~ [![Wheel](https://img.shields.io/pypi/wheel/requires.svg)](https://img.shields.io/pypi/wheel/requires.svg) [![Version](https://img.shields.io/pypi/v/requires.svg)](https://img.shields.io/pypi/v/requires.svg) [![py_versions](https://img.shields.io/pypi/pyversions/requires.svg)](https://img.shields.io/pypi/pyversions/requires.svg)

### [xtyping](./libs/xtyping/README.md) ~ `pip install xtyping` ~ [![Wheel](https://img.shields.io/pypi/wheel/xtyping.svg)](https://img.shields.io/pypi/wheel/xtyping.svg) [![Version](https://img.shields.io/pypi/v/xtyping.svg)](https://img.shields.io/pypi/v/xtyping.svg) [![py_versions](https://img.shields.io/pypi/pyversions/xtyping.svg)](https://img.shields.io/pypi/pyversions/xtyping.svg)

## Notebooks

```
notebooks/
├── cache_money.ipynb
├── filter_none.ipynb
├── json_parsing.ipynb
└── string_fmt.ipynb
```

 - [Filtering None and False-y values](./notebooks/filter_none.ipynb)
 - [cache money! `functools.lru_cache`](./notebooks/cache_money.ipynb)
 - [String formatting funks](./notebooks/string_fmt.ipynb)
 - [JSON parsing vs plain-jane dictionaries](./notebooks/json_parsing.ipynb)

## Design PhilosoPY & Principles

 - dgpy-libs must have awesome lib/pkg names and be mostly polished
 - Embrace `async/await`
 - Python 3.6 'n up, baby! Get w/ the program (the python program)
 - Write non-standard but elegant python, bc PEP 20 is lame and not fun (PEP 20: "There should be one-- and preferably only one --obvious way to do it...")
 - TYPE ANNOTATE ERR-THANG
 - Prefer pure-python & compiled-3rd-party-libs over writing packages with compiled extensions
 - Use optional compiled-3rd-party-libs as optional dependencies to sneakily speed things up if present
 - Offer integrations/extensions with the super-hot-fire modern python packages all the kids are using
 - Optional dependencies are good! Missing optional deps should trigger an error msg that is helpful to installing the relevant dependency ONLY IF THE DEPENDENCY IS NEEDED.
 - 100% test coverage `!=` good/bug-free code

## Third party packages/libs that integrate/inspire dgpy-libs

 - pydantic
 - loguru
 - httpx (forget about requests)
 - fastapi
 - attrs
 - typer
 - poetry
 - orjson
 - rapidjson/python-rapidjson
 - h5py
 - Most of the libs by aio-libs
 - rich
 - nox

___

## Contributor(s):
 
 - [Jesse Rubin](https://github.com/jessekrubin) ~ `jesse@dgi.com` / `jessekrubin@gmail.com`

## Contributing:

Plz do! Send me that PR!

___

## TODO:

 - Figure out some docs
 - Have CI/CD auto build n publish
 - Make some sort of change log
 - Publish packages to conda-forge? (maybe)

