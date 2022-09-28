<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# requires

[![Wheel](https://img.shields.io/pypi/wheel/requires.svg)](https://img.shields.io/pypi/wheel/requires.svg)
[![Version](https://img.shields.io/pypi/v/requires.svg)](https://img.shields.io/pypi/v/requires.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/requires.svg)](https://img.shields.io/pypi/pyversions/requires.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install requires`

Decorate that lets you
Require/Import dependencies at runtime.

Python dependency management can be mind bottlingly complex. Optional dependencies are pretty common. Why not require the dependency at run time if a function requires said dependency?

This package has come in handy in lambda-land where you only get 250mb (on aws)!

---

## Usage:

```python
# This will fail
def uno():
    return json.dumps({"a": 1, "b": 2})


try:
    uno()
except NameError as ne:
    print("Error:", ne)
```

    Error: name 'json' is not defined

```python
# This will not fail
import requires  # Module is callable! (checkout funkify for more info -- `pip install funkify`)


@requires("json")
def uno():
    return json.dumps({"a": 1, "b": 2})


uno()
```

    '{"a": 1, "b": 2}'

```python
import requires


@requires("from json import dumps")
def uno():
    return dumps({"a": 1, "b": 2})


uno()
```

    '{"a": 1, "b": 2}'

```python
def dos():
    return dumps({"a": 1, "b": 2})


dos()
```

    '{"a": 1, "b": 2}'

```python
import requires


@requires(_from="json", _import="dumps")
def dos():
    return dumps({"a": 1, "b": 2})


dos()
```

    '{"a": 1, "b": 2}'

```python
import requires


@requires(_import="rapidjson", pip="python-rapidjson", conda_forge="python-rapidjson")
def tres():
    return rapidjson.dumps({"a": 1, "b": 2})


tres()  # Will err if not install with where to install instructions
```

    '{"a":1,"b":2}'

```python
# should error
def quatro():
    return path.join("a", "b")


try:
    quatro()
except NameError as ne:
    print("ERROR:", ne)
```

    ERROR: name 'path' is not defined

```python
from requires import Requirement

os_path_req = Requirement(_import="path", _from="os")


@os_path_req
def quatro():
    return path.join("a", "b")


assert isinstance(quatro(), str)
```

## Enforcing requirements

```python
import requires

try:
    import alibrary
except ModuleNotFoundError:
    requirement = requires.Requirement(
        _import="alibrary",
        pip=True,
        conda_forge="alibrary-conda-listing",
        details="Install details",
    )
try:
    requirement.raise_error()
except requires.RequirementError as err:
    print("ERROR:")
    print(err)
```

    ERROR:
    Module/Package(s) not found/installed; could not import: `import alibrary`
        pip install alibrary
        conda install -c conda-forge alibrary-conda-listing
        Install details

## Less verbose version:

```python
import requires

try:
    import alibrary
except ModuleNotFoundError:
    requires.Requirement(
        _import='alibrary',
        pip=True,
        conda_forge='alibrary-conda-listing',
        details="Install details"
    ).raise_error()
```

---

## Future ideas?

- Adding support for requiring particular package versions?
- Auto install?
- Allow non pip/conda/conda-forge locations?
