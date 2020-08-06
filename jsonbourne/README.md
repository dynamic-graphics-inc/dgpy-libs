# jsonbourne

<img src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/master/_data/dgpy_logo.svg?raw=true" alt="drawing" width="120"/> **Dynamic Graphics Python**

[![Wheel](https://img.shields.io/pypi/wheel/jsonbourne.svg)](https://img.shields.io/pypi/wheel/jsonbourne.svg)
[![Version](https://img.shields.io/pypi/v/jsonbourne.svg)](https://img.shields.io/pypi/v/jsonbourne.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/jsonbourne.svg)](https://img.shields.io/pypi/pyversions/jsonbourne.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install jsonbourne`

___

## Who? What? Where? When? Why?

**WHO???** Secret agent Json Bourne

**WHAT???** Python json lib/pkg that makes json feel a little bit more like the JSON module in javascript/typescript

**WHERE???** Dynamic Graphics Inc

**WHEN???** 9 => 5 on workdays

**WHY???** Three reasons: **1)** Why not? **2)** Also I (jessekrubin) wanted a python object that was a hybrid between a dictionary and an python-object that worked kinda like a js object. **3)** Was able to get `jsonbourne` on pip

___

## Usage:

### JSON ~ `from jsonbourne import JSON`

**JSON basics:**


```python
from jsonbourne import JSON
string_stringify = JSON.stringify({"a":1, "b":2, "c":3})  # '{"a": 1, "b": 2, "c": 3}'
string_dumps = JSON.dumps({"a":1, "b":2, "c":3})  # '{"a": 1, "b": 2, "c": 3}'
string_dumps
```




    '{"a":1,"b":2,"c":3}'



#### JSON option kwargs ~ `pretty` & `sort_keys`

**pretty:**


```python
string_dumps = JSON.stringify({"b":2, "a":1, "c":3}, pretty=True)  # '{"a": 1, "b": 2, "c": 3}'
print(string_dumps)
```

    {
      "b": 2,
      "a": 1,
      "c": 3
    }


**sort_keys:**


```python
string_dumps = JSON.stringify({"b":2, "a":1, "c":3}, pretty=True, sort_keys=True)  # '{"a": 1, "b": 2, "c": 3}'
print(string_dumps)
```

    {
      "a": 1,
      "b": 2,
      "c": 3
    }


### JsonObj & JSON

- Python dictionary/object with dot access
- Create a `jsonbourne.JsonObj` with `jsonbourne.JSON`
- Recurses into sub lists/dictionaries
- Works with `pydantic.BaseModel` and `attrs`
- Allows for kwarging (`**json_obj`)



```python
import datetime

data = {
    "key": "value",
    "list": [1, 2, 3, 4, 5],
    "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    "sub": {'b': 3, 'key': 'val', 'a': 1,},
    "timedelta": datetime.timedelta(days=2),
}

JSON(data)
```




<pre>JsonObj(**{
    'dt': datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    'key': 'value',
    'list': [1, 2, 3, 4, 5],
    'sub': {'a': 1, 'b': 3, 'key': 'val'},
    'timedelta': datetime.timedelta(days=2)
})</pre>



### Dot access


```python
JSON(data).sub.b
```




    3




```python
stringified_data = JSON(data).stringify(pretty=True)
print(stringified_data)
```

    {
      "key": "value",
      "list": [
        1,
        2,
        3,
        4,
        5
      ],
      "dt": "1970-01-01T00:00:00.000001",
      "sub": {
        "b": 3,
        "key": "val",
        "a": 1
      },
      "timedelta": 172800.0
    }



```python
parsed_data = JSON(stringified_data)
parsed_data
```




<pre>JsonObj(**{
    'dt': '1970-01-01T00:00:00.000001',
    'key': 'value',
    'list': [1, 2, 3, 4, 5],
    'sub': {'a': 1, 'b': 3, 'key': 'val'},
    'timedelta': 172800.0
})</pre>




```python
list(parsed_data.keys())
```




    ['key', 'list', 'dt', 'sub', 'timedelta']




```python
list(parsed_data.items())
```




    [('key', 'value'),
     ('list', [1, 2, 3, 4, 5]),
     ('dt', '1970-01-01T00:00:00.000001'),
     ('sub', JsonObj(**{'b': 3, 'key': 'val', 'a': 1})),
     ('timedelta', 172800.0)]




```python
list(parsed_data.dot_keys())
```




    ['key', 'list', 'dt', 'sub.b', 'sub.key', 'sub.a', 'timedelta']




```python
list(parsed_data.dot_items())
```




    [('key', 'value'),
     ('list', [1, 2, 3, 4, 5]),
     ('dt', '1970-01-01T00:00:00.000001'),
     ('sub.b', 3),
     ('sub.key', 'val'),
     ('sub.a', 1),
     ('timedelta', 172800.0)]




```python
parsed_data['sub.key']
```




    'val'




```python
parsed_data.dot_lookup('sub.key')
```




    'val'




```python
{**parsed_data}
```




    {'key': 'value',
     'list': [1, 2, 3, 4, 5],
     'dt': '1970-01-01T00:00:00.000001',
     'sub': JsonObj(**{'b': 3, 'key': 'val', 'a': 1}),
     'timedelta': 172800.0}




```python
# fully eject
parsed_data.eject()
```




    {'key': 'value',
     'list': [1, 2, 3, 4, 5],
     'dt': '1970-01-01T00:00:00.000001',
     'sub': {'b': 3, 'key': 'val', 'a': 1},
     'timedelta': 172800.0}



### Usage with pydantic


```python
from jsonbourne import JsonObj
from jsonbourne.pydantic import JsonBaseModel
class JsonSubObj(JsonBaseModel):
    herm: int

    def to_dict(self):
        return self.dict()

    def to_json(self, *args, **kwargs):
        return self.json()

    @classmethod
    def from_json(cls, json_string: str):
        return JsonSubObj(json.loads(json_string))

class JsonObjModel(JsonBaseModel):
    a: int
    b: int
    c: str
    d: JsonObj
    e: JsonSubObj

    #
    @property
    def a_property(self) -> str:
        return "prop_value"

    def to_json(self, *args, **kwargs):
        return self.json()

    @classmethod
    def from_json(cls, json_string: str):
        return cls(**json.loads(json_string))

obj = JsonObjModel(
    **{"a": 1, "b": 2, "c": "herm", "d": {"nested": "nestedval"}, "e": {"herm": 2}}
)
obj
```




<pre>JsonObjModel(**{
    'a': 1, 'b': 2, 'c': 'herm', 'd': JsonObj(**{'nested': 'nestedval'}), 'e': JsonSubObj(herm=2)
})</pre>




```python
# respects properties (which I don't think pydantic does(currently))
obj.a_property
```




    'prop_value'



___

## JSON backend/lib

**`jsonbourne` finds the best json-lib (python-rapidjson/orjson) it can!** On import `jsonbourne` gets to
work spying on your python env. `jsonbourne`, the most highly qualified json-CIA-agent, will import the best
python-json library it can find; if `jsonbourne`'s cover is blown (meaning: the
only json library found is the python stdlib json), `jsonbourne` will fallback
to
the python stdlib json.

`jsonbourne` will look for the following json-packages in the following order:

  1) `rapidjson`
  2) `orjson`

### Custom lib preferences


```python
from jsonbourne import import_json
json = import_json(("rapidjson", "orjson"))  # prefer rapidjson over orjson
string = json.dumps({"a":1, "b":2, "c":3})
print(json)
print(string)
```

    <class 'jsonbourne.jsonlib._rapidjson.RAPIDJSON'>
    {"a":1,"b":2,"c":3}


### Installing better JSON lib:

#### `orjson`

- `pip install orjson` [pip]

#### `rapidjson`/`python-rapidjson`

- `pip install python-rapidjson` [pip]
- `conda install -c anaconda python-rapidjson` [conda anaconda/defaults]
- `conda install -c conda-forge python-rapidjson` [conda-forge]



```python

```
