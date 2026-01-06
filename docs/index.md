<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# dgpy-libs

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Docs:
[dynamic-graphics-inc.github.io/dgpy-libs](https://dynamic-graphics-inc.github.io/dgpy-libs/)

Repo:
[github.com/dynamic-graphics-inc/dgpy-libs](https://github.com/dynamic-graphics-inc/dgpy-libs)

---

Dynamic Graphics python libraries, home of:

- Callable modules/packages
- Recursive list/generator comprehensions
- Many decorators
- Secret agent JSON-Bourne

## Libs

```txt
libs
├── aiopen      - async file-io
├── asyncify    - async/await utilities
├── dgpylibs    - dgpy-libs mega package
├── dgpytest    - pytest plugin (WIP)
├── fmts        - string formatting tools
├── funkify     - callable modules
├── h5          - hdf5 tools
├── jsonbourne  - JSON tools/wrappers
├── lager       - logging library built on loguru
├── listless    - generator tools
├── requires    - dynamic import(s)
├── shellfish   - shell and filesystem tools
└── xtyping     - types
```

**Install:**

```bash
# pip
pip install aiopen asyncify fmts funkify h5 jsonbourne lager listless requires shellfish xtyping
# uv
uv add aiopen asyncify fmts funkify h5 jsonbourne lager listless requires shellfish xtyping
```

| Package                         | Install                  | Version                                                                                                                      | Python Versions                                                                                                                                        |
| ------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [aiopen](./libs/aiopen)         | `pip install aiopen`     | [![PyPI](https://img.shields.io/pypi/v/aiopen?style=flat-square&cacheSeconds=600)](https://pypi.org/project/aiopen/)         | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiopen?style=flat-square&cacheSeconds=600)](https://pypi.org/project/aiopen/)         |
| [asyncify](./libs/asyncify)     | `pip install asyncify`   | [![PyPI](https://img.shields.io/pypi/v/asyncify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/asyncify/)     | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asyncify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/asyncify/)     |
| [fmts](./libs/fmts)             | `pip install fmts`       | [![PyPI](https://img.shields.io/pypi/v/fmts?style=flat-square&cacheSeconds=600)](https://pypi.org/project/fmts/)             | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fmts?style=flat-square&cacheSeconds=600)](https://pypi.org/project/fmts/)             |
| [funkify](./libs/funkify)       | `pip install funkify`    | [![PyPI](https://img.shields.io/pypi/v/funkify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/funkify/)       | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/funkify?style=flat-square&cacheSeconds=600)](https://pypi.org/project/funkify/)       |
| [h5](./libs/h5)                 | `pip install h5`         | [![PyPI](https://img.shields.io/pypi/v/h5?style=flat-square&cacheSeconds=600)](https://pypi.org/project/h5/)                 | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/h5?style=flat-square&cacheSeconds=600)](https://pypi.org/project/h5/)                 |
| [jsonbourne](./libs/jsonbourne) | `pip install jsonbourne` | [![PyPI](https://img.shields.io/pypi/v/jsonbourne?style=flat-square&cacheSeconds=600)](https://pypi.org/project/jsonbourne/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jsonbourne?style=flat-square&cacheSeconds=600)](https://pypi.org/project/jsonbourne/) |
| [lager](./libs/lager)           | `pip install lager`      | [![PyPI](https://img.shields.io/pypi/v/lager?style=flat-square&cacheSeconds=600)](https://pypi.org/project/lager/)           | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lager?style=flat-square&cacheSeconds=600)](https://pypi.org/project/lager/)           |
| [listless](./libs/listless)     | `pip install listless`   | [![PyPI](https://img.shields.io/pypi/v/listless?style=flat-square&cacheSeconds=600)](https://pypi.org/project/listless/)     | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/listless?style=flat-square&cacheSeconds=600)](https://pypi.org/project/listless/)     |
| [requires](./libs/requires)     | `pip install requires`   | [![PyPI](https://img.shields.io/pypi/v/requires?style=flat-square&cacheSeconds=600)](https://pypi.org/project/requires/)     | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requires?style=flat-square&cacheSeconds=600)](https://pypi.org/project/requires/)     |
| [shellfish](./libs/shellfish)   | `pip install shellfish`  | [![PyPI](https://img.shields.io/pypi/v/shellfish?style=flat-square&cacheSeconds=600)](https://pypi.org/project/shellfish/)   | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shellfish?style=flat-square&cacheSeconds=600)](https://pypi.org/project/shellfish/)   |
| [xtyping](./libs/xtyping)       | `pip install xtyping`    | [![PyPI](https://img.shields.io/pypi/v/xtyping?style=flat-square&cacheSeconds=600)](https://pypi.org/project/xtyping/)       | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xtyping?style=flat-square&cacheSeconds=600)](https://pypi.org/project/xtyping/)       |

## About

This repo (dgpy-libs) are the polished gems formed under intense geological
pressure below the offices of [Dynamic Graphics Inc](http://dgi.com/). These
python libraries are all published on pip under the listed names.

### Design PhilosoPY

- dgpy-libs must have excellent names and be published on pip
- Embrace `async/await`
- Python 3.9+ 'n up, baby!
- Use type annotations everywhere
- No dead or commented out code
- Use optional compiled-3rd-party-libs as optional dependencies to sneakily
  speed things up if present
- Optional dependencies are good! Missing optional deps should trigger an error
  msg that is helpful to installing the relevant dependency ONLY IF THE
  DEPENDENCY IS NEEDED.
- Test coverage is usually a dumb metric and 100% test coverage `!=` bug-free
  code (tests of dgpy-libs are slowly being migrated from internal/private repos
  to this repo)

### Third party friends

- [uv](https://github.com/astral-sh/uv): the greatest thing since sliced bread
- [ruff](https://github.com/astral-sh/ruff): python linter and formatter
- [pydantic](https://pydantic-docs.helpmanual.io/): no need for explanation
- [loguru](https://github.com/Delgan/loguru): very nice python logging library
- [httpx](https://www.python-httpx.org/): http client library
- [attrs](https://github.com/python-attrs/attrs); class decorators library
- [orjson](https://github.com/ijl/orjson); fastest python json library (optional
  dep of jsonbourne)
- [rapidjson/python-rapidjson](https://github.com/python-rapidjson/python-rapidjson);
  best mostly drop-in replacement for python's json module
- [h5py](https://github.com/h5py/h5py); base of h5
- [rich](https://github.com/willmcgugan/rich); best python console formatting
  library
- [nox](https://github.com/theacodes/nox); truly a work of art

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

- [Jesse Rubin](https://github.com/jessekrubin) ~ `jesse@dgi.com` /
  `jessekrubin@gmail.com`
- [Dan Costello](https://github.com/dan-costello) ~ `dan@dgi.com` /
  `dan.costello2@gmail.com`
- Possibly you!?

## Contributing

Plz do! Send me that PR!

---

## License

All dgpy-libs are MIT licensed

```txt
dgpy-libs

The MIT License (MIT)

Copyright (c) 2019-2026 Dynamic Graphics Inc (dgi)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
