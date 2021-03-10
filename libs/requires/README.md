<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" height="120"/>
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

___

## Usage:



```python
# This will fail
def uno():
    return json.dumps({'a': 1, 'b': 2})

try:
    uno()
except NameError as ne:
    print("Error:", ne)
```

    Error: name 'json' is not defined



```python
# This will not fail
import requires  # Module is callable! (checkout funkify for more info -- `pip install funkify`)

@requires('json')
def uno():
    return json.dumps({'a': 1, 'b': 2})

uno()
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-3ffdd02e0ce4> in <module>
          1 # This will not fail
    ----> 2 import requires  # Module is callable! (checkout funkify for more info -- `pip install funkify`)
          3 
          4 @requires('json')
          5 def uno():


    /mnt/d/dgpy-dev/dgpy-libs/libs/requires/requires/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """`requires` ~ make modules callable"""
    ----> 3 from funkify import funkify
          4 from requires._meta import __version__
          5 from requires.core import (


    ModuleNotFoundError: No module named 'funkify'



```python
import requires

@requires('from json import dumps')
def uno():
    return dumps({'a': 1, 'b': 2})

uno()
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-0f4747ee5a8d> in <module>
    ----> 1 import requires
          2 
          3 @requires('from json import dumps')
          4 def uno():
          5     return dumps({'a': 1, 'b': 2})


    /mnt/d/dgpy-dev/dgpy-libs/libs/requires/requires/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """`requires` ~ make modules callable"""
    ----> 3 from funkify import funkify
          4 from requires._meta import __version__
          5 from requires.core import (


    ModuleNotFoundError: No module named 'funkify'



```python
def dos():
    return dumps({'a': 1, 'b': 2})

dos()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-c55804ca3790> in <module>
          2     return dumps({'a': 1, 'b': 2})
          3 
    ----> 4 dos()
    

    <ipython-input-1-c55804ca3790> in dos()
          1 def dos():
    ----> 2     return dumps({'a': 1, 'b': 2})
          3 
          4 dos()


    NameError: name 'dumps' is not defined



```python
import requires

@requires(_from='json', _import='dumps')
def dos():
    return dumps({'a': 1, 'b': 2})

dos()
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-50c01f9ce9df> in <module>
    ----> 1 import requires
          2 
          3 @requires(_from='json', _import='dumps')
          4 def dos():
          5     return dumps({'a': 1, 'b': 2})


    /mnt/d/dgpy-dev/dgpy-libs/libs/requires/requires/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """`requires` ~ make modules callable"""
    ----> 3 from funkify import funkify
          4 from requires._meta import __version__
          5 from requires.core import (


    ModuleNotFoundError: No module named 'funkify'



```python
import requires

@requires(_import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson')
def tres():
    return rapidjson.dumps({'a': 1, 'b': 2})

tres()  # Will err if not install with where to install instructions
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-eddc4b10b188> in <module>
    ----> 1 import requires
          2 
          3 @requires(_import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson')
          4 def tres():
          5     return rapidjson.dumps({'a': 1, 'b': 2})


    /mnt/d/dgpy-dev/dgpy-libs/libs/requires/requires/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """`requires` ~ make modules callable"""
    ----> 3 from funkify import funkify
          4 from requires._meta import __version__
          5 from requires.core import (


    ModuleNotFoundError: No module named 'funkify'



```python
# should error
def quatro():
    return path.join('a', 'b')

try:
    quatro()
except NameError as ne:
    print("ERROR:", ne)
```

    ERROR: name 'path' is not defined



```python
from requires import Requirement

os_path_req = Requirement(_import='path', _from='os')

@os_path_req
def quatro():
    return path.join('a', 'b')

assert isinstance(quatro(), str)
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-c3498d55ddec> in <module>
    ----> 1 from requires import Requirement
          2 
          3 os_path_req = Requirement(_import='path', _from='os')
          4 
          5 @os_path_req


    /mnt/d/dgpy-dev/dgpy-libs/libs/requires/requires/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """`requires` ~ make modules callable"""
    ----> 3 from funkify import funkify
          4 from requires._meta import __version__
          5 from requires.core import (


    ModuleNotFoundError: No module named 'funkify'


## Enforcing requirements


```python
import requires

try:
    import alibrary
except ModuleNotFoundError:
    requirement = requires.Requirement(
        _import='alibrary',
        pip=True,
        conda_forge='alibrary-conda-listing',
        details="Install details"
    )
try:
    requirement.raise_error()
except requires.RequirementError as err:
    print("ERROR:")
    print(err)
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-1-fb7ad22150e0> in <module>
    ----> 1 import requires
          2 
          3 try:
          4     import alibrary
          5 except ModuleNotFoundError:


    /mnt/d/dgpy-dev/dgpy-libs/libs/requires/requires/__init__.py in <module>
          1 # -*- coding: utf-8 -*-
          2 """`requires` ~ make modules callable"""
    ----> 3 from funkify import funkify
          4 from requires._meta import __version__
          5 from requires.core import (


    ModuleNotFoundError: No module named 'funkify'


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


___

## Future ideas?

 - Adding support for requiring particular package versions?
 - Auto install?
 - Allow non pip/conda/conda-forge locations?
