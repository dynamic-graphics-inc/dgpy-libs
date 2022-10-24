<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# dgpy-libs

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dynamic-graphics-inc/dgpy-libs/main?filepath=README.ipynb)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Docs: [dynamic-graphics-inc.github.io/dgpy-libs](https://dynamic-graphics-inc.github.io/dgpy-libs/)

Repo: [github.com/dynamic-graphics-inc/dgpy-libs](https://github.com/dynamic-graphics-inc/dgpy-libs)

---

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

**Install:** `pip install aiopen asyncify funkify h5 jsonbourne lager requires xtyping`

### [aiopen](./libs/aiopen) ~ `pip install aiopen` ~ [![Wheel](https://img.shields.io/pypi/wheel/aiopen.svg)](https://img.shields.io/pypi/wheel/aiopen.svg) [![Version](https://img.shields.io/pypi/v/aiopen.svg)](https://img.shields.io/pypi/v/aiopen.svg) [![py_versions](https://img.shields.io/pypi/pyversions/aiopen.svg)](https://img.shields.io/pypi/pyversions/aiopen.svg)

### [asyncify](./libs/asyncify) ~ `pip install asyncify` ~ [![Wheel](https://img.shields.io/pypi/wheel/asyncify.svg)](https://img.shields.io/pypi/wheel/asyncify.svg) [![Version](https://img.shields.io/pypi/v/asyncify.svg)](https://img.shields.io/pypi/v/asyncify.svg) [![py_versions](https://img.shields.io/pypi/pyversions/asyncify.svg)](https://img.shields.io/pypi/pyversions/asyncify.svg)

### [funkify](./libs/funkify) ~ `pip install funkify` ~ [![Wheel](https://img.shields.io/pypi/wheel/funkify.svg)](https://img.shields.io/pypi/wheel/funkify.svg) [![Version](https://img.shields.io/pypi/v/funkify.svg)](https://img.shields.io/pypi/v/funkify.svg) [![py_versions](https://img.shields.io/pypi/pyversions/funkify.svg)](https://img.shields.io/pypi/pyversions/funkify.svg)

### [h5](./libs/h5) ~ `pip install h5` ~ [![Wheel](https://img.shields.io/pypi/wheel/h5.svg)](https://img.shields.io/pypi/wheel/h5.svg) [![Version](https://img.shields.io/pypi/v/h5.svg)](https://img.shields.io/pypi/v/h5.svg) [![py_versions](https://img.shields.io/pypi/pyversions/h5.svg)](https://img.shields.io/pypi/pyversions/h5.svg)

### [jsonbourne](./libs/jsonbourne) ~ `pip install jsonbourne` ~ [![Wheel](https://img.shields.io/pypi/wheel/jsonbourne.svg)](https://img.shields.io/pypi/wheel/jsonbourne.svg) [![Version](https://img.shields.io/pypi/v/jsonbourne.svg)](https://img.shields.io/pypi/v/jsonbourne.svg) [![py_versions](https://img.shields.io/pypi/pyversions/jsonbourne.svg)](https://img.shields.io/pypi/pyversions/jsonbourne.svg)

### [lager](./libs/lager) ~ `pip install lager` ~ [![Wheel](https://img.shields.io/pypi/wheel/lager.svg)](https://img.shields.io/pypi/wheel/lager.svg) [![Version](https://img.shields.io/pypi/v/lager.svg)](https://img.shields.io/pypi/v/lager.svg) [![py_versions](https://img.shields.io/pypi/pyversions/lager.svg)](https://img.shields.io/pypi/pyversions/lager.svg)

### [requires](./libs/requires) ~ `pip install requires` ~ [![Wheel](https://img.shields.io/pypi/wheel/requires.svg)](https://img.shields.io/pypi/wheel/requires.svg) [![Version](https://img.shields.io/pypi/v/requires.svg)](https://img.shields.io/pypi/v/requires.svg) [![py_versions](https://img.shields.io/pypi/pyversions/requires.svg)](https://img.shields.io/pypi/pyversions/requires.svg)

### [xtyping](./libs/xtyping) ~ `pip install xtyping` ~ [![Wheel](https://img.shields.io/pypi/wheel/xtyping.svg)](https://img.shields.io/pypi/wheel/xtyping.svg) [![Version](https://img.shields.io/pypi/v/xtyping.svg)](https://img.shields.io/pypi/v/xtyping.svg) [![py_versions](https://img.shields.io/pypi/pyversions/xtyping.svg)](https://img.shields.io/pypi/pyversions/xtyping.svg)

## About

This repo (dgpy-libs) are the polished gems formed under intense pressure below the offices of [Dynamic Grahpics Inc](http://dgi.com/). These pure-python libraries are all published on pip under the listed names.

### Design PhilosoPY

- dgpy-libs must have excellent names and be published on pip
- Embrace `async/await`
- Python 3.6 'n up, baby! (May move to 3.7 for `__future___.annotations`... tbd)
- Use type annotations everywhere
- No dead or commented out code
- Prefer pure-python & compiled-3rd-party-libs over writing packages with compiled extensions
- Use optional compiled-3rd-party-libs as optional dependencies to sneakily speed things up if present
- Offer integrations with the super-hot-fire modern python packages all the kids are using
- Optional dependencies are good! Missing optional deps should trigger an error msg that is helpful to installing the relevant dependency ONLY IF THE DEPENDENCY IS NEEDED.
- Test coverage is usually a dumb metric and 100% test coverate `!=` bug-free code (tests of dgpy-libs are slowly being migrated from internal/private repos to this repo)

### Third party friends

- [pydantic](https://pydantic-docs.helpmanual.io/); best python lib you will ever use
- [loguru](https://github.com/Delgan/loguru); base of lager
- [httpx](https://www.python-httpx.org/) ; don't use requests
- [fastapi](https://github.com/tiangolo/fastapi); best python web server framework
- [attrs](https://github.com/python-attrs/attrs); pydantic alternative
- [typer](https://github.com/tiangolo/typer); awesome cli framework
- [poetry](https://github.com/python-poetry/poetry); best dep management python has to offer
- [orjson](https://github.com/ijl/orjson); fastest python json lib (opt dep of jsonbourne)
- [rapidjson/python-rapidjson](https://github.com/python-rapidjson/python-rapidjson); best mostly drop-in replacement for python's json module
- [h5py](https://github.com/h5py/h5py); base of h5
- [rich](https://github.com/willmcgugan/rich); best python console formatting lib
- [nox](https://github.com/theacodes/nox); like tox but less maddening

---

## Notebooks

```
notebooks/
├── cache_money.ipynb
├── filter_none.ipynb
├── json_parsing.ipynb
└── string_fmt.ipynb
```

- [Filtering None and False-y values](./notebooks/filter_none)
- [cache money! `functools.lru_cache`](./notebooks/cache_money)
- [String formatting funks](./notebooks/string_fmt)
- [JSON parsing vs plain-jane dictionaries](./notebooks/json_parsing)

---

## Contributor(s):

- [Jesse Rubin](https://github.com/jessekrubin) ~ `jesse@dgi.com` / `jessekrubin@gmail.com`

## Contributing:

Plz do! Send me that PR!

---

## TODO:

- Have CI/CD auto build n publish
- Make some sort of change log
