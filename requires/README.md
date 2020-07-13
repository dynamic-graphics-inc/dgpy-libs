# requires

<img src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_logo.svg?raw=true" alt="drawing" width="120"/> **Dynamic Graphics Python**

[![Wheel](https://img.shields.io/pypi/wheel/requires.svg)](https://img.shields.io/pypi/wheel/requires.svg)
[![Version](https://img.shields.io/pypi/v/requires.svg)](https://img.shields.io/pypi/v/requires.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/requires.svg)](https://img.shields.io/pypi/pyversions/requires.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install requires`

___

## Who? What? Where? When? Why?

**WHO???** jesse @ dgi

**WHAT???** (tiny) Lib/package with decorator that lets you require/import dependencies at runtime.

**WHERE???** Dynamic Graphics Inc

**WHEN???** 9 => 5 on workdays

**WHY???** Python dependency management can be mind bottlingly complex, and many projects I (jesse) work on end up having optional dependencies. Why not require the dependency at run time if a function requires said dependency?


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

    ModuleNotFoundError                       Traceback (most recent call last)

    /mnt/d/dgpy-dev/dgpy-libs/requires/requires/core.py in _requires_dec(*args, **kwargs)
        146                 if self.alias not in _f_globals:
    --> 147                     _f_globals[self.alias] = self.import_requirement()
        148                 retval = f(*args, **kwargs)


    /mnt/d/dgpy-dev/dgpy-libs/requires/requires/core.py in import_requirement(self)
         99         if self._from is None:
    --> 100             return import_module(self._import)
        101         req = import_module(self._from)


    ~/miniconda3/envs/dgpy/lib/python3.8/importlib/__init__.py in import_module(name, package)
        126             level += 1
    --> 127     return _bootstrap._gcd_import(name[level:], package, level)
        128 


    ~/miniconda3/envs/dgpy/lib/python3.8/importlib/_bootstrap.py in _gcd_import(name, package, level)


    ~/miniconda3/envs/dgpy/lib/python3.8/importlib/_bootstrap.py in _find_and_load(name, import_)


    ~/miniconda3/envs/dgpy/lib/python3.8/importlib/_bootstrap.py in _find_and_load_unlocked(name, import_)


    ModuleNotFoundError: No module named 'rapidjson'

    
    During handling of the above exception, another exception occurred:


    RequirementError                          Traceback (most recent call last)

    <ipython-input-6-eddc4b10b188> in <module>
          5     return rapidjson.dumps({'a': 1, 'b': 2})
          6 
    ----> 7 tres()  # Will err if not install with where to install instructions
    

    /mnt/d/dgpy-dev/dgpy-libs/requires/requires/core.py in _requires_dec(*args, **kwargs)
        149                 return retval
        150             except ModuleNotFoundError:
    --> 151                 raise self.err()
        152 
        153         return _requires_dec


    RequirementError: Module/Package(s) not found/installed; could not import: `import rapidjson`
        pip install python-rapidjson
        conda install -c conda-forge python-rapidjson



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


