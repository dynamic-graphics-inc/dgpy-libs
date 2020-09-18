# requires

<img src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_banner.svg?raw=true" alt="drawing" width="320"/>

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

uno()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-ec67aed17342> in <module>
          3     return json.dumps({'a': 1, 'b': 2})
          4 
    ----> 5 uno()
    

    <ipython-input-1-ec67aed17342> in uno()
          1 # This will fail
          2 def uno():
    ----> 3     return json.dumps({'a': 1, 'b': 2})
          4 
          5 uno()


    NameError: name 'json' is not defined



```python
# This will not fail
import requires  # Module is callable! (checkout funkify for more info -- `pip install funkify`)

@requires('json')
def uno():
    return json.dumps({'a': 1, 'b': 2})

uno()
```




    '{"a": 1, "b": 2}'




```python
import requires

@requires('from json import dumps')
def uno():
    return dumps({'a': 1, 'b': 2})

uno()
```




    '{"a": 1, "b": 2}'




```python
def dos():
    return dumps({'a': 1, 'b': 2})

dos()
```




    '{"a": 1, "b": 2}'




```python
import requires

@requires(_from='json', _import='dumps')
def dos():
    return dumps({'a': 1, 'b': 2})

dos()
```




    '{"a": 1, "b": 2}'




```python
import requires

@requires(_import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson')
def tres():
    return rapidjson.dumps({'a': 1, 'b': 2})

tres()  # Will err if not install with where to install instructions
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-6-eddc4b10b188> in <module>
          5     return rapidjson.dumps({'a': 1, 'b': 2})
          6 
    ----> 7 tres()  # Will err if not install with where to install instructions
    

    <ipython-input-6-eddc4b10b188> in tres()
          3 @requires(_import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson')
          4 def tres():
    ----> 5     return rapidjson.dumps({'a': 1, 'b': 2})
          6 
          7 tres()  # Will err if not install with where to install instructions


    NameError: name 'rapidjson' is not defined



```python
# should error
def quatro():
    return path.join('a', 'b')

quatro()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-7-b3f241a5c6c7> in <module>
          3     return path.join('a', 'b')
          4 
    ----> 5 quatro()
    

    <ipython-input-7-b3f241a5c6c7> in quatro()
          1 # should error
          2 def quatro():
    ----> 3     return path.join('a', 'b')
          4 
          5 quatro()


    NameError: name 'path' is not defined



```python
from requires import Requirement

os_path_req = Requirement(_import='path', _from='os')

@os_path_req
def quatro():
    return path.join('a', 'b')

quatro()
```




    'a/b'


