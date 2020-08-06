# -*- coding: utf-8 -*-
"""Json Bourne -- EZ-PZ-JSON with lots o goodies"""
import keyword
import sys

from itertools import chain
from pprint import pformat
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Optional,
    Set,
    Tuple,
)

from jsonbourne import json


if sys.version_info < (3, 7):
    from collections.abc import MutableMapping

    JsonObjMutableMapping = MutableMapping
else:
    from typing import MutableMapping

    JsonObjMutableMapping = MutableMapping[str, Any]

__all__ = [
    "JsonObj",
    "JsonDict",
    "JsonObjMutableMapping",
    "stringify",
    "parse",
    "jsonify",
    "JSON",
]


def is_identifier(string: str) -> bool:
    """Return True if a string is a valid python identifier; False otherwise

    Args:
        string (str): String (likely to be used as a key) to check

    Returns:
        bool: True if is an identifier

    Examples:
        >>> is_identifier("herm")
        True
        >>> is_identifier("something that contains spaces")
        False
        >>> is_identifier("import")
        False
        >>> is_identifier("something.with.periods")
        False
        >>> is_identifier("astring-with-dashes")
        False
        >>> is_identifier("astring_with_underscores")
        True
        >>> is_identifier(123)
        False

    """
    try:
        assert isinstance(string, str)
    except AssertionError:
        return False
    if not string.isidentifier():
        return False
    if keyword.iskeyword(string):
        return False
    return True


class JsonObj(JsonObjMutableMapping):
    """JSON friendly python dictionary with dot notation and string only keys

    JsonObj(foo='bar')['foo'] == JsonObj(foo='bar').foo

    Examples:
        >>> d = {"uno": 1, "dos": 2, "tres": 3}
        >>> d
        {'uno': 1, 'dos': 2, 'tres': 3}
        >>> d = JsonObj(d)
        >>> d
        JsonObj(**{'uno': 1, 'dos': 2, 'tres': 3})
        >>> list(d.keys())
        ['uno', 'dos', 'tres']
        >>> list(d.dot_keys())
        ['uno', 'dos', 'tres']
        >>> d
        JsonObj(**{'uno': 1, 'dos': 2, 'tres': 3})
        >>> d['uno']
        1
        >>> d.uno
        1
        >>> d['uno'] == d.uno
        True
        >>> d.uno = "ONE"
        >>> d
        JsonObj(**{'uno': 'ONE', 'dos': 2, 'tres': 3})
        >>> d['uno'] == d.uno
        True
        >>> 'uno' in d
        True
        >>> 'not_in_d' in d
        False
        >>> d
        JsonObj(**{'uno': 'ONE', 'dos': 2, 'tres': 3})
        >>> del d['dos']
        >>> d
        JsonObj(**{'uno': 'ONE', 'tres': 3})
        >>> del d.tres
        >>> d
        JsonObj(**{'uno': 'ONE'})
        >>> d = {"uno": 1, "dos": 2, "tres": {"a": 1, "b": [3, 4, 5, 6]}}
        >>> d = JsonObj(d)
        >>> d
        JsonObj(**{'uno': 1, 'dos': 2, 'tres': {'a': 1, 'b': [3, 4, 5, 6]}})
        >>> d.tres
        JsonObj(**{'a': 1, 'b': [3, 4, 5, 6]})
        >>> d.tres.a
        1
        >>> d.tres.a = "new-val"
        >>> d.tres.a
        'new-val'
        >>> d
        JsonObj(**{'uno': 1, 'dos': 2, 'tres': {'a': 'new-val', 'b': [3, 4, 5, 6]}})
        >>> jd = JsonObj({"a":1, "b": 'herm', 'alist':[{'sub': 123}]})

        It does lists!? oh my

        >>> jd
        JsonObj(**{'a': 1, 'b': 'herm', 'alist': [{'sub': 123}]})
        >>> jd.alist[0]
        JsonObj(**{'sub': 123})
        >>> jd.eject()
        {'a': 1, 'b': 'herm', 'alist': [{'sub': 123}]}

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Use the object dict"""
        self.__dict__.update(*args, **kwargs)
        try:
            assert all(isinstance(k, str) for k in self.__dict__)
        except AssertionError:
            d = {k: v for k, v in self.__dict__.items() if not isinstance(k, str)}
            raise ValueError(
                "JsonObj keys MUST be strings! Bad key values: {}".format(str(d))
            )
        self.recurse()

    def recurse(self) -> None:
        """Recusively convert all sub dictionaries to JsonObj objects"""
        self.__dict__.update({k: jsonify(v) for k, v in self.__dict__.items()})

    def __attrs_post_init__(self) -> None:
        self.recurse()

    def __contains__(self, key: str) -> bool:  # type: ignore
        """Check if a key or dot-key is contained within the JsonObj object

        Args:
            key (str): root level key or a dot-key

        Returns:
            bool: True if the key/dot-key is in the JsonObj; False otherwise

        Examples:
            >>> d = {"uno": 1, "dos": 2, "tres": 3, "sub": {"a": 1, "b": 2, "c": [3, 4, 5, 6], "d": "a_string"}}
            >>> d = JsonObj(d)
            >>> d
            JsonObj(**{'uno': 1, 'dos': 2, 'tres': 3, 'sub': {'a': 1, 'b': 2, 'c': [3, 4, 5, 6], 'd': 'a_string'}})
            >>> 'uno' in d
            True
            >>> 'this_key_is_not_in_d' in d
            False
            >>> 'sub.a' in d
            True
            >>> 'sub.d.a' in d
            False

        """
        if "." in key:
            first_key, _, rest = key.partition(".")
            val = self.__dict__.get(first_key)
            return isinstance(val, MutableMapping) and val.__contains__(rest)
        return key in self.__dict__

    def __setitem__(self, key: str, value: Any) -> None:
        """Set JsonObj item with 'key' to 'value'

        Args:
            key (str): Key/item to set
            value: Value to set

        Returns:
            None

        Raises:
            ValueError: If given a key that is not a valid python keyword/identifier

        Examples:
            >>> d = JsonObj()
            >>> d.a = 123
            >>> d['b'] = 321
            >>> d
            JsonObj(**{'a': 123, 'b': 321})
            >>> d[123] = 'a'
            Traceback (most recent call last):
            ...
            ValueError: Invalid key: (123).
            Key cannot be integer or convertable to integer
            >>> d['123'] = 'a'
            Traceback (most recent call last):
            ...
            ValueError: Invalid key: (123).
            Key(s) is not a valid python identifier

        """
        if isinstance(key, int):
            raise ValueError(
                f"Invalid key: ({key}).\n"
                f"Key cannot be integer or convertable to integer"
            )

        if not is_identifier(key):
            raise ValueError(
                f"Invalid key: ({key}).\n" f"Key(s) is not a valid python identifier"
            )
        self.__dict__[key] = value

    def __getattr__(self, item: str) -> Any:
        """Return an attr

        Examples:
            >>> d = {
            ...     'falsey_dict': {},
            ...     'falsey_list': [],
            ...     'falsey_string': '',
            ...     'is_false': False,
            ...     'a': None,
            ...     'b': 2,
            ...     'c': {
            ...         'd': 'herm',
            ...         'e': None,
            ...         'falsey_dict': {},
            ...         'falsey_list': [],
            ...         'falsey_string': '',
            ...         'is_false': False,
            ...     },
            ...     }
            ...
            >>> d = JsonObj(d)
            >>> d.__getattr__('b')
            2

        """
        try:
            return self.__dict__[item]
        except KeyError:
            pass
        return object.__getattribute__(self, item)

    def __getattribute__(self, item: str) -> Any:
        return object.__getattribute__(self, item)

    def __getitem__(self, key: str) -> Any:
        if "." in key:
            return self.dot_lookup(key)
        try:
            return jsonify(self.__dict__[key])
        except KeyError:
            pass
        try:
            return jsonify(object.__getattribute__(self, key))
        except AttributeError:
            raise KeyError(str(key))

    def __delitem__(self, key: str) -> None:
        del self.__dict__[key]

    def __iter__(self) -> Iterator[Any]:
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)

    def items(self) -> ItemsView[str, Any]:
        """Return an items view of the JsonObj object"""
        return self.__dict__.items()

    def entries(self) -> ItemsView[str, Any]:
        """Alias for items"""
        return self.items()

    def keys(self) -> KeysView[str]:
        """Return the keys view of the JsonObj object"""
        return self.__dict__.keys()

    def filter_none(self, recursive: bool = False) -> "JsonObj":
        """Filter key-values where the value is `None` but not false-y

        Args:
            recursive (bool): Recursively filter out None values

        Returns:
            JsonObj that has been filtered of None values

        Examples:
            >>> d = {
            ...     'falsey_dict': {},
            ...     'falsey_list': [],
            ...     'falsey_string': '',
            ...     'is_false': False,
            ...     'a': None,
            ...     'b': 2,
            ...     'c': {
            ...         'd': 'herm',
            ...         'e': None,
            ...         'falsey_dict': {},
            ...         'falsey_list': [],
            ...         'falsey_string': '',
            ...         'is_false': False,
            ...     },
            ...     }
            ...
            >>> d = JsonObj(d)
            >>> print(d)
            JsonObj(**{
                'a': None,
                'b': 2,
                'c': {'d': 'herm',
                      'e': None,
                      'falsey_dict': {},
                      'falsey_list': [],
                      'falsey_string': '',
                      'is_false': False},
                'falsey_dict': {},
                'falsey_list': [],
                'falsey_string': '',
                'is_false': False
            })
            >>> print(d.filter_none())
            JsonObj(**{
                'b': 2,
                'c': {'d': 'herm',
                      'e': None,
                      'falsey_dict': {},
                      'falsey_list': [],
                      'falsey_string': '',
                      'is_false': False},
                'falsey_dict': {},
                'falsey_list': [],
                'falsey_string': '',
                'is_false': False
            })
            >>> from pprint import pprint
            >>> print(d.filter_none(recursive=True))
            JsonObj(**{
                'b': 2,
                'c': {'d': 'herm',
                      'falsey_dict': {},
                      'falsey_list': [],
                      'falsey_string': '',
                      'is_false': False},
                'falsey_dict': {},
                'falsey_list': [],
                'falsey_string': '',
                'is_false': False
            })

        """
        if recursive:
            return JsonObj(
                {
                    k: v
                    if not isinstance(v, (dict, JsonObj))
                    else JsonObj(v).filter_none(recursive=True)
                    for k, v in self.items()
                    if v is not None
                }
            )
        return JsonObj({k: v for k, v in self.items() if v is not None})

    def filter_false(self, recursive: bool = False) -> "JsonObj":
        """Filter key-values where the value is false-y

        Args:
            recursive (bool): Recurse into sub JsonObjs and dictionaries

        Returns:
            JsonObj that has been filtered

        Examples:
            >>> d = {
            ...     'falsey_dict': {},
            ...     'falsey_list': [],
            ...     'falsey_string': '',
            ...     'is_false': False,
            ...     'a': None,
            ...     'b': 2,
            ...     'c': {
            ...         'd': 'herm',
            ...         'e': None,
            ...         'falsey_dict': {},
            ...         'falsey_list': [],
            ...         'falsey_string': '',
            ...         'is_false': False,
            ...     },
            ...     }
            ...
            >>> d = JsonObj(d)
            >>> print(d)
            JsonObj(**{
                'a': None,
                'b': 2,
                'c': {'d': 'herm',
                      'e': None,
                      'falsey_dict': {},
                      'falsey_list': [],
                      'falsey_string': '',
                      'is_false': False},
                'falsey_dict': {},
                'falsey_list': [],
                'falsey_string': '',
                'is_false': False
            })
            >>> print(d.filter_false())
            JsonObj(**{
                'b': 2,
                'c': {'d': 'herm',
                      'e': None,
                      'falsey_dict': {},
                      'falsey_list': [],
                      'falsey_string': '',
                      'is_false': False}
            })
            >>> print(d.filter_false(recursive=True))
            JsonObj(**{
                'b': 2, 'c': {'d': 'herm'}
            })

        """
        if recursive:
            return JsonObj(
                {
                    k: v
                    if not isinstance(v, (dict, JsonObj))
                    else JsonObj(v).filter_false(recursive=True)
                    for k, v in self.items()
                    if v
                }
            )
        return JsonObj({k: v for k, v in self.items() if v})

    def dot_keys(self) -> Iterable[str]:
        """Yield the JsonObj's dot-notation keys

        Returns:
            Iterable[str]: List of the dot-notation friendly keys


        The Non-chain version (shown below) is very slightly slower than the
        `itertools.chain` version.

        NON-CHAIN VERSION:

        for k, value in self.items():
            value = jsonify(value)
            if isinstance(value, JsonObj):
                yield from (f"{k}.{dk}" for dk in value.dot_keys())
            else:
                yield k

        """
        return chain(  # type: ignore
            *(
                (str(k),)
                if not isinstance(v, JsonObj)
                else (*(f"{k}.{dk}" for dk in jsonify(v).dot_keys()),)
                for k, v in self.items()
            )
        )

    def dot_keys_list(self, sort_keys: bool = False) -> List[str]:
        """Return a list of the JsonObj's dot-notation friendly keys

        Args:
            sort_keys (bool): Flag to have the dot-keys be returned sorted

        Returns:
            List[str]: List of the dot-notation friendly keys

        """
        if sort_keys:
            return sorted(self.dot_keys_list())
        return list(self.dot_keys())

    def dot_keys_set(self) -> Set[str]:
        """Return a set of the JsonObj's dot-notation friendly keys

        Returns:
            Set[str]: List of the dot-notation friendly keys

        """
        return set(self.dot_keys())

    def dot_lookup(self, dot_key: str) -> Any:
        """Look up JsonObj keys using dot notation as a string

        Args:
            dot_key (str): dot-notation key to look up ('key1.key2.third_key')

        Returns:
            The result of the dot-notation key look up

        Raises:
            KeyError: Raised if the dot-key is not in in the object

        """
        parts = dot_key.split(".")
        root_val: Any = self.__dict__.get(parts[0])
        cur_val = root_val
        for ix, part in enumerate(parts[1:], start=1):
            try:
                cur_val = cur_val[part]
            except TypeError:
                reached = ".".join(parts[:ix])
                raise KeyError(
                    f"Invalid DotKey: {dot_key} -- Lookup reached: {reached} => {str(cur_val)}"
                )
        return cur_val

    def dot_items(self) -> Iterator[Tuple[str, Any]]:
        """Yield tuples of the form (dot-key, value)"""
        return ((dk, self.dot_lookup(dk)) for dk in self.dot_keys())

    def to_str(self, minify: bool = False, width: int = 88) -> str:
        """Return a string representation of the JsonObj object"""
        if minify:
            return type(self).__name__ + "(**" + str(self.to_dict()) + ")"
        return "".join(
            [
                type(self).__name__,
                "(**{\n    ",
                pformat(self.to_dict(), width=width)[1:-1].replace("\n", "\n   "),
                "\n})",
            ]
        )

    def __repr__(self) -> str:
        """Return the string representation of the object"""
        return self.to_str(minify=True)

    def __str__(self) -> str:
        """Return the string representation of the JsonObj object"""
        return self.to_str(minify=False)

    def _repr_html_(self) -> str:
        """Return the HTML representation of the JsonObj object"""
        return "<pre>{}</pre>".format(self.__str__())

    @classmethod
    def _cls_attr_names(cls) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        try:
            return {el.name for el in cls.__attrs_attrs__}  # type: ignore
        except AttributeError:
            raise AttributeError("Class is not decorated with attr.attrs")

    @classmethod
    def _cls_fields(cls) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        try:
            return cls.__fields__  # type: ignore
        except AttributeError:
            raise AttributeError("Class does not inherit from pydantic.BaseModel")

    @classmethod
    def _cls_field_names(cls) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        try:
            return {el for el in cls.__fields__}  # type: ignore
        except AttributeError:
            raise AttributeError("Class does not inherit from pydantic.BaseModel")

    def _field_names(self) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        return self.__class__._cls_field_names()

    def eject(self) -> Dict[str, Any]:
        """Eject to python-builtin dictionary object

        Examples:
            >>> d = JsonObj(**{'uno': 'ONE', 'tres': 3, 'dos': 2})
            >>> d
            JsonObj(**{'uno': 'ONE', 'tres': 3, 'dos': 2})
            >>> plain_ol_dict = d.eject()
            >>> plain_ol_dict
            {'uno': 'ONE', 'tres': 3, 'dos': 2}
            >>> type(plain_ol_dict)
            <class 'dict'>

        """
        return {
            k: unjsonify(v)
            # if not isinstance(v, JsonObj) else v.eject()
            for k, v in self.__dict__.items()
        }

    def to_dict(self) -> Dict[str, Any]:
        """Return the JsonObj object (and children) as a python dictionary"""
        return self.eject()

    def asdict(self) -> Dict[str, Any]:
        """Return the JsonObj object (and children) as a python dictionary"""
        return self.eject()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JsonObj":
        """Return a JsonObj object from a dictionary of data"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_string: str) -> "JsonObj":
        """Return a JsonObj object from a json string

        Args:
            json_string (str): JSON string to convert to a JsonObj

        Returns:
            JsonObj: JsonObj object for the given JSON string

        """
        return cls.from_json(json_string)

    @classmethod
    def _from_json(cls, json_string: str) -> "JsonObj":
        """Return a JsonObj object from a json string

        Args:
            json_string (str): JSON string to convert to a JsonObj

        Returns:
            JsonObj: JsonObj object for the given JSON string

        """
        return cls.from_dict(json.loads(json_string))

    def to_json(
        self, pretty: bool = False, sort_keys: bool = False, **kwargs: Any
    ) -> str:
        """Return a JSON string of the JsonObj object

        Args:
            minify (bool): Return a 'minified' version of the JSON string
            sort_keys (bool): Sort the keys when converting to JSON
            indent (int): Indent level of the json string
            **kwargs: Keyword args to be passed on to the JSON dumps method

        Returns:
            str: JSON string of the JsonObj object

        """
        return self._to_json(pretty=pretty, sort_keys=sort_keys, **kwargs)

    def stringify(
        self, pretty: bool = False, sort_keys: bool = False, **kwargs: Any
    ) -> str:
        """Return a JSON string of the JsonObj; `JsonObj.to_json` alias

        Args:
            pretty (bool): If a 'minified' version of the JSON string
            sort_keys (bool): Sort the keys when converting to JSON
            **kwargs: Keyword args to be passed on to the JSON dumps method

        Returns:
            str: JSON string of the JsonObj object

        """
        return self.to_json(pretty=pretty, sort_keys=sort_keys, **kwargs)

    def _to_json(
        self, pretty: bool = False, sort_keys: bool = False, **kwargs: Any
    ) -> str:
        """Return a JSON string of the JsonObj object

        Args:
            minify (bool): Return a 'minified' version of the JSON string
            sort_keys (bool): Sort the keys when converting to JSON
            indent (int): Indent level of the json string
            **kwargs: Keyword args to be passed on to the JSON dumps method

        Returns:
            str: JSON string of the JsonObj object

        """
        return json.dumps(self.to_dict(), pretty=pretty, sort_keys=sort_keys, **kwargs)

    @classmethod
    def validate_type(cls, val: Any) -> "JsonObj":
        """Validate and convert a value to a JsonObj object"""
        return JsonObj(val)

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], Any]]:
        """Return the JsonObj validator functions"""
        yield cls.validate_type


class JsonDict(JsonObj):
    """Alias for JsonObj"""

    pass


def jsonify(value: Any) -> Any:
    """Convert and return a value to a JsonObj if the value is a dict"""
    if isinstance(value, dict) and not isinstance(value, JsonObj):
        return JsonObj(value)
    if isinstance(value, list):
        return [jsonify(el) for el in value]
    if isinstance(value, tuple):
        return tuple([jsonify(el) for el in value])
    if isinstance(value, str):
        try:
            data = json.loads(value)
            return jsonify(data)
        except Exception:
            pass

    return value


def unjsonify(value: Any) -> Any:
    """Recursively eject a JsonDit object"""
    if isinstance(value, JsonObj):
        return {k: unjsonify(v) for k, v in value.__dict__.items()}
    if isinstance(value, list):
        return [unjsonify(el) for el in value]
    if isinstance(value, tuple):
        return tuple([unjsonify(el) for el in value])
    return value


class JSONMeta(type):
    """Meta type for use by JSON class to allow for static `__call__` method"""

    @staticmethod
    def __call__(value: Any):  # type: ignore
        return jsonify(value)


class JSON(metaclass=JSONMeta):
    """JSON class meant to mimic the js/ts-JSON"""

    @staticmethod
    def stringify(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return str(
            json.dumps(
                data, pretty=pretty, sort_keys=sort_keys, default=default, **kwargs
            )
        )

    @staticmethod
    def dumps(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return str(
            json.dumps(
                data, pretty=pretty, sort_keys=sort_keys, default=default, **kwargs
            )
        )

    @staticmethod
    def binify(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return bytes(
            json.dumpb(
                data, pretty=pretty, sort_keys=sort_keys, default=default, **kwargs
            )
        )

    @staticmethod
    def dumpb(
        data: Any,
        pretty: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        return bytes(
            json.dumpb(
                data, pretty=pretty, sort_keys=sort_keys, default=default, **kwargs
            )
        )

    @staticmethod
    def loads(string: str, obj: bool = False, **kwargs: Any) -> Any:
        if obj:
            return jsonify(json.loads(string, **kwargs))
        return json.loads(string, **kwargs)

    @staticmethod
    def parse(string: str, obj: bool = True) -> Any:
        if obj:
            return jsonify(json.loads(string))
        return json.loads(string)

    @staticmethod
    def json_lib() -> Any:
        return json._json.__class__.__name__


class JSONModuleCls(ModuleType, JSON):
    @staticmethod
    def __call__(value: Any):  # type: ignore
        return jsonify(value)


stringify = JSON.stringify
parse = JSON.parse
