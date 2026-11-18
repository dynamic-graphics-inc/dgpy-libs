# JSON & python

## Here is a dictionary...

We can create this dictionary by writing it as python code (like below).

We could also create the same dictionary by `json.loads`-ing a json string of the same dictionary.

It turns out that parsing a json string is MUCH faster than creating the dictionary as a python literal


```python
data = {
    "id": 1,
    "code": None,
    "subd": {"a": 23, "b": {"herm": 2}},
    "type": "foo",
    "bars": [
        {"id": 6934900},
        {"id": 6934977},
        {"id": 6934992},
        {"id": 6934993},
        {"id": 6935014},
    ],
    "n": 10,
    "date_str": "2013-07-08 00:00:00",
    "float_here": 0.454545,
    "complex": [{"id": 83865, "goal": "herm", "state": "active"}],
    "profile_id": None,
    "state": "active",
}
```

___

## Creating a python literal dictionary for python to parse


```python
data_python_str = str(data)
data_python_str  # here is our string
```




    "{'id': 1, 'code': None, 'subd': {'a': 23, 'b': {'herm': 2}}, 'type': 'foo', 'bars': [{'id': 6934900}, {'id': 6934977}, {'id': 6934992}, {'id': 6934993}, {'id': 6935014}], 'n': 10, 'date_str': '2013-07-08 00:00:00', 'float_here': 0.454545, 'complex': [{'id': 83865, 'goal': 'herm', 'state': 'active'}], 'profile_id': None, 'state': 'active'}"



___

## Creating a JSON string to parse


```python
import json

data_json_string = json.dumps(data)
data_json_string
```




    '{"id": 1, "code": null, "subd": {"a": 23, "b": {"herm": 2}}, "type": "foo", "bars": [{"id": 6934900}, {"id": 6934977}, {"id": 6934992}, {"id": 6934993}, {"id": 6935014}], "n": 10, "date_str": "2013-07-08 00:00:00", "float_here": 0.454545, "complex": [{"id": 83865, "goal": "herm", "state": "active"}], "profile_id": null, "state": "active"}'



## NOTE: The json string and the python string look almost identical


```python
try:
    print(parsed_dict_str)
except NameError:
    print("'parsed_dict_str' is not defined ... yet ...")
```

    'parsed_dict_str' is not defined ... yet ...



```python
parse_and_set_data_python_str = "parsed_dict_str = " + data_python_str
print("This is the python string we are going to execute to do the parsing:")
parse_and_set_data_python_str
```

    This is the python string we are going to execute to do the parsing:





    "parsed_dict_str = {'id': 1, 'code': None, 'subd': {'a': 23, 'b': {'herm': 2}}, 'type': 'foo', 'bars': [{'id': 6934900}, {'id': 6934977}, {'id': 6934992}, {'id': 6934993}, {'id': 6935014}], 'n': 10, 'date_str': '2013-07-08 00:00:00', 'float_here': 0.454545, 'complex': [{'id': 83865, 'goal': 'herm', 'state': 'active'}], 'profile_id': None, 'state': 'active'}"



___

## Parsing the dictionary string w/ python


```python
exec(parse_and_set_data_python_str)
print("NOW IT IS DEFINED")
parsed_dict_str
```

    NOW IT IS DEFINED





    {'id': 1,
     'code': None,
     'subd': {'a': 23, 'b': {'herm': 2}},
     'type': 'foo',
     'bars': [{'id': 6934900},
      {'id': 6934977},
      {'id': 6934992},
      {'id': 6934993},
      {'id': 6935014}],
     'n': 10,
     'date_str': '2013-07-08 00:00:00',
     'float_here': 0.454545,
     'complex': [{'id': 83865, 'goal': 'herm', 'state': 'active'}],
     'profile_id': None,
     'state': 'active'}



## They are the same!


```python
parsed_dict_str == data
```




    True



___

## Parsing the JSON string dictionary


```python
json_parsed_data = json.loads(data_json_string)
print("---")
print("DATA PARSED VIA JSON:", json_parsed_data)
print("---")
print(f"JSON PARSED DATA == DICT PARSED DATA: {json_parsed_data == parsed_dict_str}")
```

    ---
    DATA PARSED VIA JSON: {'id': 1, 'code': None, 'subd': {'a': 23, 'b': {'herm': 2}}, 'type': 'foo', 'bars': [{'id': 6934900}, {'id': 6934977}, {'id': 6934992}, {'id': 6934993}, {'id': 6935014}], 'n': 10, 'date_str': '2013-07-08 00:00:00', 'float_here': 0.454545, 'complex': [{'id': 83865, 'goal': 'herm', 'state': 'active'}], 'profile_id': None, 'state': 'active'}
    ---
    JSON PARSED DATA == DICT PARSED DATA: True


___

# It's time to time

## First up parsing the python dictionary as a string


```python
%%timeit
exec(parse_and_set_data_python_str)
```

    67.6 µs ± 2.2 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


## Second parsing the json string


```python
%%timeit
# NBVAL_IGNORE_OUTPUT
json_parsed_data = json.loads(data_json_string)
```

    7.34 µs ± 1.52 µs per loop (mean ± std. dev. of 7 runs, 100000 loops each)


# The JSON parsing is WAY faster... but there are faster json libs for python

## Lets try python-rapidjson


```python
%%timeit
# NBVAL_IGNORE_OUTPUT
import rapidjson

json_parsed_data = rapidjson.loads(data_json_string)
```

    7.52 µs ± 152 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)


## Lets try ujson


```python
%%timeit
# NBVAL_IGNORE_OUTPUT
import ujson

json_parsed_data = ujson.loads(data_json_string)
```

    4.16 µs ± 114 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)


## Lets try orjson


```python
%%timeit
# NBVAL_IGNORE_OUTPUT
import orjson

json_parsed_data = orjson.loads(data_json_string)
```

    4.01 µs ± 197 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
