<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# jsonbourne

[![Wheel](https://img.shields.io/pypi/wheel/jsonbourne.svg)](https://img.shields.io/pypi/wheel/jsonbourne.svg)
[![Version](https://img.shields.io/pypi/v/jsonbourne.svg)](https://img.shields.io/pypi/v/jsonbourne.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/jsonbourne.svg)](https://img.shields.io/pypi/pyversions/jsonbourne.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install jsonbourne`

- Python json lib/pkg that makes json feel like the JSON module in javascript/typescript:
  - `from jsonbourne import JSON; JSON.parse(JSON.stringify({"key": "value"}))`
  - Automatically uses best json-lib-backend available (`orjson`/`python-rapidjson`) ~ can be configured
- Hybrid dict/class object (`jsonbourne.JsonObj`):
  - Dot-notation getting/setting (featuring protected attributes!)
  - All your favorite python dictionary methods (`items`, `keys`, `update`, `values`) and more!
  - Works with `pydantic` and `attrs`
- FastAPI:
  - JSONBOURNEResponse ~ auto use the best
- No hard dependencies ~ works with python-stdlib-json as well as `orjson` and `python-rapidjson`
- `jsonbourne.JsonObj` uses list/dict comprehensions (some are recursive) everywhere because 'why not?' and it is a bit faster

## Usage:

### JSON ~ `from jsonbourne import JSON`

**Importing:**

```python
# Importing JSON:
from jsonbourne import JSON

# or
import JSON

# Importing jsonbourne:
import jsonbourne
import david_webb  # jsonbourne's `True` identity
```

**JSON basics:**

```python
import JSON  # Module included with jsonbourne

string_stringify = JSON.stringify(
    {"a": 1, "b": 2, "c": 3}
)  # '{"a": 1, "b": 2, "c": 3}'
string_dumps = JSON.dumps({"a": 1, "b": 2, "c": 3})  # '{"a": 1, "b": 2, "c": 3}'
string_dumps
```

    '{"a":1,"b":2,"c":3}'

#### JSON option kwargs ~ `pretty` & `sort_keys`

**pretty:**

```python
string_dumps = JSON.stringify(
    {"b": 2, "a": 1, "c": 3}, pretty=True
)  # '{"a": 1, "b": 2, "c": 3}'
print(string_dumps)
```

    {
      "b": 2,
      "a": 1,
      "c": 3
    }

**sort_keys:**

```python
string_dumps = JSON.stringify(
    {"b": 2, "a": 1, "c": 3}, pretty=True, sort_keys=True
)  # '{"a": 1, "b": 2, "c": 3}'
print(string_dumps)
```

    {
      "a": 1,
      "b": 2,
      "c": 3
    }

### JsonObj & JSON

- Python dictionary/object with dot access
- Protections against setting class/obj attributes
- Is as javascript-y as possible (keys have to be strings -- ints/floats will be converted to strings)
- Create a `jsonbourne.JsonObj` with `jsonbourne.JSON`
- Recursive jsonification
- Allows for kwarging (`**json_obj`)
- Works with `pydantic` and `attrs`

#### Make an empty JsonObj

The following 3 examples all produce the same thing

```python
from jsonbourne import JSON
j = JSON()  # j => JsonObj(**{})
# OR
import JSON
j = JSON()  # j => JsonObj(**{})
# OR
from jsonbourne import JsonObj
j = JsonObj()  # j => JsonObj(**{})
```

#### From a dictionary o data

```python
import datetime

data = {
    "key": "value",
    "list": [1, 2, 3, 4, 5],
    "dt": datetime.datetime(1970, 1, 1, 0, 0, 0, 1),
    "sub": {
        "b": 3,
        "key": "val",
        "a": 1,
    },
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

    [('key',),
     ('list',),
     ('dt',),
     ('sub', 'b'),
     ('sub', 'key'),
     ('sub', 'a'),
     ('timedelta',)]

```python
list(parsed_data.dot_items())
```

    [(('key',), 'value'),
     (('list',), [1, 2, 3, 4, 5]),
     (('dt',), '1970-01-01T00:00:00.000001'),
     (('sub', 'b'), 3),
     (('sub', 'key'), 'val'),
     (('sub', 'a'), 1),
     (('timedelta',), 172800.0)]

```python
parsed_data[("sub", "key")]
```

    'val'

```python
parsed_data.dot_lookup("sub.key")
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

#### Protected keys

`jsonbourne.JsonObj` protects against setting attributes like `'items'` through dot-notation.

```python
from jsonbourne import JSON

j = JSON()
j.key = "value"
try:  # CANNOT set 'items' using dot-access
    j.items = [1, 2, 3, 4]
except ValueError:
    pass
# CAN set 'items' through key/item access
j["items"] = [1, 2, 3, 4]
print(j.__dict__)
print(j)
j_items = j.items
print("items", j_items)
# Getting 'items' through dot-access returns the `items()` method
assert j.items != [1, 2, 3, 4]
# Getting 'items' with key-access returns the stored value
assert j["items"] == [1, 2, 3, 4]
```

    {'_data': {'key': 'value', 'items': [1, 2, 3, 4]}}
    JsonObj(**{
        'items': [1, 2, 3, 4], 'key': 'value'
    })
    items <bound method JsonObj.items of JsonObj(**{'key': 'value', 'items': [1, 2, 3, 4]})>

### pydantic & jsonbourne

- `from jsonbourne.pydantic import JsonBaseModel`
- Allows for aliases when getting/setting attribute(s)
- Supports `__post_init__` (like dataclasses)

#### Basic usage:

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
     'a': 1,
     'b': 2,
     'c': 'herm',
     'd': JsonObj(**{'nested': 'nestedval'}),
     'e': {'herm': 2}
})</pre>

```python
# respects properties (which I don't think pydantic does(currently))
obj.a_property
```

    'prop_value'

---

## JSON backend/lib

**`jsonbourne` finds the best json-lib (python-rapidjson/orjson) it can!** On import `jsonbourne` gets to
work spying on your python env. `jsonbourne`, the most highly qualified json-CIA-agent, will import the best
python-json library it can find; if `jsonbourne`'s cover is blown (meaning: the
only json library found is the python stdlib json), `jsonbourne` will fallback
to
the python stdlib json.

`jsonbourne` will look for the following json-packages in the following order:

1. `rapidjson`
2. `orjson`

### Custom lib preferences

```python
from jsonbourne import import_json

json = import_json(("rapidjson", "orjson"))  # prefer rapidjson over orjson
string = json.dumps({"a": 1, "b": 2, "c": 3})
print(json)
print(string)
```

    <class 'jsonbourne.jsonlib.RAPIDJSON'>
    {"a":1,"b":2,"c":3}

### Installing better JSON lib:

#### `orjson`

- `pip install orjson` [pip]

#### `rapidjson`/`python-rapidjson`

- `pip install python-rapidjson` [pip]
- `conda install -c anaconda python-rapidjson` [conda anaconda/defaults]
- `conda install -c conda-forge python-rapidjson` [conda-forge]
