<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# dgpy-libs

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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

```txt
libs
├── aiopen
├── asyncify
├── dgpylibs
├── dgpytest
├── fmts
├── funkify
├── h5
├── jsonbourne
├── lager
├── listless
├── requires
├── shellfish
└── xtyping
```

**Install:**

```bash
# pip
pip install aiopen asyncify fmts funkify h5 jsonbourne lager listless requires shellfish xtyping
# uv
uv add aiopen asyncify fmts funkify h5 jsonbourne lager listless requires shellfish xtyping
```

| Package | Install | Version | Python Versions |
|--------|---------|---------|-----------------|
| [aiopen](./libs/aiopen) | `pip install aiopen` | [![PyPI](https://img.shields.io/pypi/v/aiopen?style=flat-square&cacheSeconds=600)](https://pypi.org/project/aiopen/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiopen?style=flat-square&cacheSeconds=600)](https://pypi.org/project/aiopen/) |
| [asyncify](./libs/asyncify) | `pip install asyncify` | [![PyPI](https://img.shields.io/pypi/v/asyncify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/asyncify/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asyncify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/asyncify/) |
| [fmts](./libs/fmts) | `pip install fmts` | [![PyPI](https://img.shields.io/pypi/v/fmts?style=flat-square&cacheSeconds=600)](https://pypi.org/project/fmts/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fmts?style=flat-square&cacheSeconds=600)](https://pypi.org/project/fmts/) |
| [funkify](./libs/funkify) | `pip install funkify` | [![PyPI](https://img.shields.io/pypi/v/funkify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/funkify/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/funkify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/funkify/) |
| [h5](./libs/h5) | `pip install h5` | [![PyPI](https://img.shields.io/pypi/v/h5?style=flat-square&cacheSeconds=600)](https://pypi.org/project/h5/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/h5?style=flat-square&cacheSeconds=600)](https://pypi.org/project/h5/) |
| [jsonbourne](./libs/jsonbourne) | `pip install jsonbourne` | [![PyPI](https://img.shields.io/pypi/v/jsonbourne?style=flat-square&cacheSeconds=600)](https://pypi.org/project/jsonbourne/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonbourne?style=flat-square&cacheSeconds=600)](https://pypi.org/project/jsonbourne/) |
| [lager](./libs/lager) | `pip install lager` | [![PyPI](https://img.shields.io/pypi/v/lager?style=flat-square&cacheSeconds=600)](https://pypi.org/project/lager/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lager?style=flat-square&cacheSeconds=600)](https://pypi.org/project/lager/) |
| [listless](./libs/listless) | `pip install listless` | [![PyPI](https://img.shields.io/pypi/v/listless?style=flat-square&cacheSeconds=600)](https://pypi.org/project/listless/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/listless?style=flat-square&cacheSeconds=600)](https://pypi.org/project/listless/) |
| [requires](./libs/requires) | `pip install requires` | [![PyPI](https://img.shields.io/pypi/v/requires?style=flat-square&cacheSeconds=600)](https://pypi.org/project/requires/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requires?style=flat-square&cacheSeconds=600)](https://pypi.org/project/requires/) |
| [shellfish](./libs/shellfish) | `pip install shellfish` | [![PyPI](https://img.shields.io/pypi/v/shellfish?style=flat-square&cacheSeconds=600)](https://pypi.org/project/shellfish/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shellfish?style=flat-square&cacheSeconds=600)](https://pypi.org/project/shellfish/) |
| [xtyping](./libs/xtyping) | `pip install xtyping` | [![PyPI](https://img.shields.io/pypi/v/xtyping?style=flat-square&cacheSeconds=600)](https://pypi.org/project/xtyping/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xtyping?style=flat-square&cacheSeconds=600)](https://pypi.org/project/xtyping/) |


## About

This repo (dgpy-libs) are the polished gems formed under intense pressure below the offices of [Dynamic Graphics Inc](http://dgi.com/). These pure-python libraries are all published on pip under the listed names.

### Design PhilosoPY

- dgpy-libs must have excellent names and be published on pip
- Embrace `async/await`
- Python 3.9+ 'n up, baby!
- Use type annotations everywhere
- No dead or commented out code
- Prefer pure-python & compiled-3rd-party-libs over writing packages with compiled extensions
- Use optional compiled-3rd-party-libs as optional dependencies to sneakily speed things up if present
- Optional dependencies are good! Missing optional deps should trigger an error msg that is helpful to installing the relevant dependency ONLY IF THE DEPENDENCY IS NEEDED.
- Test coverage is usually a dumb metric and 100% test coverage `!=` bug-free code (tests of dgpy-libs are slowly being migrated from internal/private repos to this repo)

### Third party friends

- [pydantic](https://pydantic-docs.helpmanual.io/); best python lib you will ever use
- [loguru](https://github.com/Delgan/loguru); base of lager
- [httpx](https://www.python-httpx.org/) ; don't use requests
- [attrs](https://github.com/python-attrs/attrs); pydantic alternative
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

## Contributor(s)

- [Jesse Rubin](https://github.com/jessekrubin) ~ `jesse@dgi.com` / `jessekrubin@gmail.com`
- [Dan Costello](https://github.com/dan-costello) ~ `dan@dgi.com` / `dan.costello2@gmail.com`
- Possibly you!?

## Contributing

Plz do! Send me that PR!

---

## TODO

- Have CI/CD auto build n publish
- Changelog (for real)
- Figure out why the combine-prs workflow doesn't trigger github actions...
- Update mkdocs to include all dgpy-libs
