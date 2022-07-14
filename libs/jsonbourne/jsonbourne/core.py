# -*- coding: utf-8 -*-
"""Json Bourne -- EZ-PZ-JSON with lots o goodies"""
from __future__ import annotations

import keyword

from functools import lru_cache
from itertools import chain
from json import JSONDecodeError
from pprint import pformat
from shutil import get_terminal_size
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from jsonbourne import jsonlib

JsonPrimitiveT = TypeVar("JsonPrimitiveT", str, int, float, None)
JsonObjT = TypeVar("JsonObjT", bound="JsonObj[Any]")
KT = TypeVar("KT")
VT = TypeVar("VT")
_KT = str
_VT = TypeVar("_VT")
JsonObjMutableMapping = MutableMapping[str, _VT]

__all__ = (
    "JsonObj",
    "JsonDict",
    "JsonObjMutableMapping",
    "stringify",
    "parse",
    "jsonify",
    "JSON",
    "UNDEFINED",
    "undefined",
    "Null",
    "null",
    "JSONModuleCls",
    "JsonObjT",
)

_JsonObjMutableMapping_attrs = set(dir(JsonObjMutableMapping))

UNDEFINED = "undefined"
undefined = "undefined"
null = None
Null = None.__class__


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


def is_float(value: Any) -> bool:
    """Return True if value is a float"""
    try:
        float(value)
        return True
    except ValueError:
        pass
    return False


def is_int(value: Any) -> bool:
    """Return True if value is a int"""
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value.is_integer()
    _value: str = str(value)
    if _value[0] in ("-", "+"):
        return str(_value[1:]).isdigit()
    return _value.isdigit()


def is_number(value: Any) -> bool:
    """Return True if value is a number"""
    return is_int(value) or is_float(value)


class JsonObj(MutableMapping[str, _VT], Generic[_VT]):
    """JSON friendly python dictionary with dot notation and string only keys

    JsonObj(foo='bar')['foo'] == JsonObj(foo='bar').foo

    Examples:
        >>> print(JsonObj())
        JsonObj(**{})
        >>> d = {"uno": 1, "dos": 2, "tres": 3}
        >>> d
        {'uno': 1, 'dos': 2, 'tres': 3}
        >>> d = JsonObj(d)
        >>> d
        JsonObj(**{'uno': 1, 'dos': 2, 'tres': 3})
        >>> list(d.keys())
        ['uno', 'dos', 'tres']
        >>> list(d.dot_keys())
        [('uno',), ('dos',), ('tres',)]
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
        >>> d.tres
        3
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

    _data: Dict[_KT, _VT]

    @overload
    def __init__(
        self,
        *args: Mapping[_KT, _VT],
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        *args: Mapping[_KT, _VT],
        **kwargs: _VT,
    ) -> None:
        ...

    def __init__(
        self,
        *args: Any,
        **kwargs: _VT,
    ) -> None:
        """Use the object dict"""
        _data = dict(*args, **kwargs)
        super().__setattr__("_data", _data)
        try:
            assert all(isinstance(k, str) for k in self._data)
        except AssertionError:
            d = {k: v for k, v in self._data.items() if not isinstance(k, str)}  # type: ignore[redundant-expr]
            raise ValueError(
                "JsonObj keys MUST be strings! Bad key values: {}".format(str(d))
            )
        self.recurse()
        self.__post_init__()

    def recurse(self) -> None:
        """Recusively convert all sub dictionaries to JsonObj objects"""
        self._data.update({k: jsonify(v) for k, v in self._data.items()})

    def __attrs_post_init__(self) -> None:
        self.recurse()

    def __post_init__(self) -> Any:
        """Function place holder that is called after object initialization"""
        pass  # pylint: disable=unnecessary-pass

    def __contains__(self, key: _KT) -> bool:  # type: ignore[override]
        """Check if a key or dot-key is contained within the JsonObj object

        Args:
            key (_KT): root level key or a dot-key

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
            val = self._data.get(first_key)
            return isinstance(val, MutableMapping) and val.__contains__(rest)
        return key in self._data

    def __setattr__(self, attr: _KT, value: _VT) -> None:
        if attr in self._cls_protected_attrs():
            raise ValueError(
                f"Cannot set protected attribute ('{str(attr)}'),"
                f" must use brackets/setitem syntax: json_obj['{str(attr)}']"
            )
        return self.__setitem__(attr, value)

    def __setitem__(self, key: _KT, value: _VT) -> None:
        """Set JsonObj item with 'key' to 'value'

        Args:
            key (_KT): Key/item to set
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
            >>> d
            JsonObj(**{'a': 123, 'b': 321, '123': 'a'})
            >>> d['456'] = 'a'
            >>> d
            JsonObj(**{'a': 123, 'b': 321, '123': 'a', '456': 'a'})

        """
        if is_int(key):
            self._data[str(key)] = value
            return None
        if not is_identifier(key):
            raise ValueError(
                f"Invalid key: ({key}).\n" f"Key(s) is not a valid python identifier"
            )
        self._data[key] = value

    def __getattr__(self, item: _KT) -> Any:
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
            >>> d.b
            2

        """
        if item == "_data":
            try:
                return object.__getattribute__(self, "_data")
            except AttributeError:
                return self.__dict__
        if item in _JsonObjMutableMapping_attrs or item in self._cls_protected_attrs():
            return object.__getattribute__(self, item)
        try:
            return jsonify(self.__getitem__(str(item)))
        except KeyError:
            pass
        return object.__getattribute__(self, item)

    def __object_getattribute__(self, item: str) -> Any:
        return object.__getattribute__(self, item)

    def __getitem__(self, key: Union[_KT, Tuple[_KT, ...]]) -> Any:
        if isinstance(key, str):
            try:
                return jsonify(self._data[key])
            except KeyError:
                pass
            try:
                return jsonify(self.__object_getattribute__(key))
            except AttributeError:
                pass
        try:
            return self.dot_lookup(key)
        except KeyError:
            ...
        raise KeyError(str(key))

    def __delitem__(self, key: _KT) -> None:
        return self._data.__delitem__(key)

    def __delattr__(self, item: _KT) -> None:
        return self.__delitem__(item)

    def __iter__(self) -> Iterator[_KT]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def items(self) -> ItemsView[_KT, _VT]:
        """Return an items view of the JsonObj object"""
        return self._data.items()

    def entries(self) -> ItemsView[_KT, _VT]:
        """Alias for items"""
        return self.items()

    def keys(self) -> KeysView[_KT]:
        """Return the keys view of the JsonObj object"""
        return self._data.keys()

    def setdefault(self, key: _KT, default: Optional[_VT] = None) -> _VT:
        if default:
            return self._data.setdefault(key, default)
        return self._data.setdefault(key)  # type: ignore[call-arg]

    def clear(self) -> None:
        self._data.clear()

    def pop(self, key: _KT, default: Optional[Any] = None) -> Any:
        if default:
            return self._data.pop(key, default)
        return self._data.pop(key)

    def get(self, key: _KT, default: Optional[Any] = None) -> Any:
        try:
            return self._data.get(key)
        except KeyError as ke:
            if default:
                return default
            raise ke

    def filter_none(self, recursive: bool = False) -> JsonObj[_VT]:
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
                cast(
                    Dict[str, _VT],
                    {
                        k: v
                        if not isinstance(v, (dict, JsonObj))
                        else JsonObj(v).filter_none(recursive=True)
                        for k, v in self.items()
                        if v is not None  # type: ignore[redundant-expr]
                    },
                )
            )
        return JsonObj({k: v for k, v in self.items() if v is not None})  # type: ignore[redundant-expr]

    def filter_false(self, recursive: bool = False) -> JsonObj[_VT]:
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
                cast(
                    Dict[str, _VT],
                    {
                        k: v
                        if not isinstance(v, (dict, JsonObj))
                        else JsonObj(v).filter_false(recursive=True)
                        for k, v in self.items()
                        if v
                    },
                )
            )
        return JsonObj({k: v for k, v in self.items() if v})

    def dot_keys(self) -> Iterable[Tuple[str, ...]]:
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
        return chain(
            *(
                ((str(k),),)
                if not isinstance(v, JsonObj)
                else (*((str(k), *dk) for dk in jsonify(v).dot_keys()),)
                for k, v in self.items()
            )
        )

    def dot_keys_list(self, sort_keys: bool = False) -> List[Tuple[str, ...]]:
        """Return a list of the JsonObj's dot-notation friendly keys

        Args:
            sort_keys (bool): Flag to have the dot-keys be returned sorted

        Returns:
            List[str]: List of the dot-notation friendly keys

        """
        if sort_keys:
            return sorted(self.dot_keys_list())
        return list(self.dot_keys())

    def dot_keys_set(self) -> Set[Tuple[str, ...]]:
        """Return a set of the JsonObj's dot-notation friendly keys

        Returns:
            Set[str]: List of the dot-notation friendly keys

        """
        return set(self.dot_keys())

    def dot_lookup(self, key: Union[str, Tuple[str, ...], List[str]]) -> Any:
        """Look up JsonObj keys using dot notation as a string

        Args:
            key (str): dot-notation key to look up ('key1.key2.third_key')

        Returns:
            The result of the dot-notation key look up

        Raises:
            KeyError: Raised if the dot-key is not in in the object
            ValueError: Raised if key is not a str/Tuple[str, ...]/List[str]

        """
        if not isinstance(key, (str, list, tuple)):
            raise ValueError(
                "".join(
                    (
                        "dot_key arg must be string or sequence of strings; ",
                        "strings will be split on '.'",
                    )
                )
            )
        parts = key.split(".") if isinstance(key, str) else list(key)
        root_val: Any = self._data[parts[0]]
        cur_val = root_val
        for ix, part in enumerate(parts[1:], start=1):
            try:
                cur_val = cur_val[part]
            except TypeError:
                reached = ".".join(parts[:ix])
                err_msg = f"Invalid DotKey: {key} -- Lookup reached: {reached} => {str(cur_val)}"
                if isinstance(key, str):
                    err_msg += "".join(
                        (
                            f"\nNOTE!!! lookup performed with string ('{key}') ",
                            "PREFER lookup using List[str] or Tuple[str, ...]",
                        )
                    )
                raise KeyError(err_msg)
        return cur_val

    def dot_items(self) -> Iterator[Tuple[Tuple[str, ...], _VT]]:
        """Yield tuples of the form (dot-key, value)

        OG-version:
            def dot_items(self) -> Iterator[Tuple[str, Any]]:
                return ((dk, self.dot_lookup(dk)) for dk in self.dot_keys())

        Readable-version:
            for k, value in self.items():
                value = jsonify(value)
                if isinstance(value, JsonObj) or hasattr(value, 'dot_items'):
                    yield from ((f"{k}.{dk}", dv) for dk, dv in value.dot_items())
                else:
                    yield k, value
        """

        return chain.from_iterable(
            (
                (
                    *(
                        (
                            (
                                str(k),
                                *dk,
                            ),
                            dv,
                        )
                        for dk, dv in as_json_obj(v).dot_items()
                    ),
                )
                if isinstance(v, (JsonObj, dict))
                else (((str(k),), v),)
                for k, v in self.items()
            )
        )

    def dot_items_list(self) -> List[Tuple[Tuple[str, ...], Any]]:
        """Return list of tuples of the form (dot-key, value)"""
        return list(self.dot_items())

    def __bool__(self) -> bool:
        return bool(self._data)

    def _is_empty(self) -> bool:
        return not bool(self._data)

    def to_str(self, minify: bool = False, width: Optional[int] = None) -> str:
        """Return a string representation of the JsonObj object"""
        if minify:
            return type(self).__name__ + "(**" + str(self.to_dict()) + ")"
        if not bool(self._data):
            return f"{type(self).__name__}(**{{}})"
        _width = get_terminal_size(fallback=(88, 24)).columns - 12
        return "".join(
            [
                type(self).__name__,
                "(**{\n    ",
                pformat(self.to_dict(), width=_width)[1:-1].replace("\n", "\n   "),
                "\n})",
            ]
        ).replace("JsonObj(**{}),", "{},")

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
            return {el.name for el in cls.__attrs_attrs__}  # type: ignore[attr-defined]
        except AttributeError:
            raise AttributeError("Class is not decorated with attr.attrs")

    @classmethod
    def _cls_fields(cls) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        try:
            return cls.__fields__  # type: ignore[attr-defined, no-any-return]
        except AttributeError:
            raise AttributeError("Class does not inherit from pydantic.BaseModel")

    @classmethod
    def _cls_field_names(cls) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        try:
            return set(cls.__fields__)  # type: ignore[attr-defined]
        except AttributeError:
            raise AttributeError("Class does not inherit from pydantic.BaseModel")

    @classmethod
    def _cls_protected_attrs(cls) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        return {
            "asdict",
            "clear",
            "copy",
            "dot_items",
            "dot_items_list",
            "dot_keys",
            "dot_keys_list",
            "dot_keys_set",
            "dot_lookup",
            "eject",
            "entries",
            "filter_false",
            "filter_none",
            "from_dict",
            "from_json",
            "fromkeys",
            "get",
            "items",
            "keys",
            "pop",
            "popitem",
            "recurse",
            "setdefault",
            "stringify",
            "to_dict",
            "to_json",
            "to_str",
            "update",
            "validate_type",
            "values",
        }

    def _field_names(self) -> Set[str]:
        """Return attrs-attribute names for an object decorated with attrs"""
        return self.__class__._cls_field_names()

    def eject(self) -> Dict[_KT, _VT]:
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
        try:
            return {k: unjsonify(v) for k, v in self._data.items()}
        except RecursionError:
            raise ValueError(
                "JSON.stringify recursion err; cycle/circular-refs detected"
            )

    def to_dict(self) -> Dict[_KT, Any]:
        """Return the JsonObj object (and children) as a python dictionary"""
        return self.eject()

    def asdict(self) -> Dict[_KT, Any]:
        """Return the JsonObj object (and children) as a python dictionary"""
        return self.eject()

    @classmethod
    def from_dict(cls: Type[JsonObj[_VT]], data: Dict[_KT, _VT]) -> JsonObj[_VT]:
        """Return a JsonObj object from a dictionary of data"""
        return cls(**data)

    @classmethod
    def from_json(
        cls: Type[JsonObj[_VT]], json_string: Union[bytes, str]
    ) -> JsonObj[_VT]:
        """Return a JsonObj object from a json string

        Args:
            json_string (str): JSON string to convert to a JsonObj

        Returns:
            JsonObjT: JsonObj object for the given JSON string

        """
        return cls._from_json(json_string)

    @classmethod
    def _from_json(
        cls: Type[JsonObj[_VT]], json_string: Union[bytes, str]
    ) -> JsonObj[_VT]:
        """Return a JsonObj object from a json string

        Args:
            json_string (str): JSON string to convert to a JsonObj

        Returns:
            JsonObjT: JsonObj object for the given JSON string

        """
        return cls.from_dict(jsonlib.loads(json_string))

    def JSON(
        self,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Return JSON string of the JsonObj object (and children)

        Args:
            fmt (bool): If True, return a JSON string with newlines and indentation
            pretty (bool): If True, return a JSON string with newlines and indentation
            sort_keys (bool): Sort dictionary keys if True
            append_newline (bool): Append a newline '\n' to JSON string if True
            default: default function hook for JSON serialization
            **kwargs (Any): additional kwargs to be passed down to jsonlib.dumps

        Returns:
            str: JSON string of the JsonObj object

        """
        return jsonlib.dumps(
            self.to_dict(),
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    def to_json(
        self,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Return JSON string of the JsonObj object (and children)

        Args:
            fmt (bool): If True, return a JSON string with newlines and indentation
            pretty (bool): If True, return a JSON string with newlines and indentation
            sort_keys (bool): Sort dictionary keys if True
            append_newline (bool): Append a newline '\n' to JSON string if True
            default: default function hook for JSON serialization
            **kwargs (Any): additional kwargs to be passed down to jsonlib.dumps

        Returns:
            str: JSON string of the JsonObj object

        """
        return self._to_json(
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    def stringify(
        self,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Return JSON string of the JsonObj object (and children)

        Args:
            fmt (bool): If True, return a JSON string with newlines and indentation
            pretty (bool): If True, return a JSON string with newlines and indentation
            sort_keys (bool): Sort dictionary keys if True
            append_newline (bool): Append a newline '\n' to JSON string if True
            default: default function hook for JSON serialization
            **kwargs (Any): additional kwargs to be passed down to jsonlib.dumps

        Returns:
            str: JSON string of the JsonObj object

        """
        return self._to_json(
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    def _to_json(
        self,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Return JSON string of the JsonObj object (and children)

        Args:
            fmt (bool): If True, return a JSON string with newlines and indentation
            pretty (bool): If True, return a JSON string with newlines and indentation
            sort_keys (bool): Sort dictionary keys if True
            append_newline (bool): Append a newline '\n' to JSON string if True
            default: default function hook for JSON serialization
            **kwargs (Any): additional kwargs to be passed down to jsonlib.dumps

        Returns:
            str: JSON string of the JsonObj object

        """

        return jsonlib.dumps(
            self.to_dict(),
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    @classmethod
    def validate_type(cls: Type[JsonObj[_VT]], val: Any) -> JsonObj[_VT]:
        """Validate and convert a value to a JsonObj object"""
        return cls(val)

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], Any]]:
        """Return the JsonObj validator functions"""
        yield cls.validate_type


class JsonDict(JsonObj[_VT], Generic[_VT]):
    """Alias for JsonObj"""

    pass


def as_json_obj(value: Union[JsonObj[_VT], Dict[_KT, _VT]]) -> JsonObj[_VT]:
    if isinstance(value, dict):
        return JsonObj(value)
    return value


@overload
def jsonify(value: JsonPrimitiveT) -> JsonPrimitiveT:
    ...


@overload
def jsonify(value: List[JsonPrimitiveT]) -> List[JsonPrimitiveT]:
    ...


@overload
def jsonify(value: Tuple[JsonPrimitiveT, ...]) -> Tuple[JsonPrimitiveT, ...]:
    ...


@overload
def jsonify(value: _VT) -> _VT:
    ...


def jsonify(value: Any) -> Any:
    """Convert and return a value to a JsonObj if the value is a dict"""
    if isinstance(value, (JsonObj, JsonDict)) or issubclass(value.__class__, JsonObj):
        return value
    if isinstance(value, dict) and not isinstance(value, JsonObj):
        return JsonObj(value)
    if isinstance(value, list):
        return [jsonify(el) for el in value]
    if isinstance(value, tuple):
        return tuple([jsonify(el) for el in value])
    if isinstance(value, str):
        try:
            data = jsonlib.loads(value)
            return jsonify(data)
        except Exception:
            pass

    return value


def unjsonify(value: Any) -> Any:
    """Recursively eject a JsonDit object"""
    if isinstance(value, JsonObj):
        return value._data
    if isinstance(value, list):
        return [unjsonify(el) for el in value]
    if isinstance(value, tuple):
        return tuple([unjsonify(el) for el in value])
    return value


class JSONMeta(type):
    """Meta type for use by JSON class to allow for static `__call__` method"""

    @staticmethod
    def __call__(value: Optional[Any] = None) -> Any:  # type: ignore[override]
        if value is None:
            value = {}
        return jsonify(value)


class JSON(metaclass=JSONMeta):
    """JSON class meant to mimic the js/ts-JSON"""

    undefined: str = UNDEFINED
    UNDEFINED: str = UNDEFINED
    null = null
    Null = Null
    JSONDecodeError = JSONDecodeError

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        return cls.__call__(*args, **kwargs)

    @staticmethod
    def stringify(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Return JSON stringified/dumps-ed data"""
        return str(
            jsonlib.dumps(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default,
                **kwargs,
            )
        )

    @staticmethod
    def dumps(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Return JSON stringified/dumps-ed data"""
        return str(
            jsonlib.dumps(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default,
                **kwargs,
            )
        )

    @staticmethod
    def binify(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        """Return JSON string bytes for given data"""
        return bytes(
            jsonlib.dumpb(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default,
                **kwargs,
            )
        )

    @staticmethod
    def dumpb(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> bytes:
        """Return JSON string bytes for given data"""
        return bytes(
            jsonlib.dumpb(
                data,
                fmt=fmt,
                pretty=pretty,
                sort_keys=sort_keys,
                append_newline=append_newline,
                default=default,
                **kwargs,
            )
        )

    @staticmethod
    def jsoncp(
        data: Any,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> Any:
        return jsonlib.jsoncp(
            data=data,
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    @staticmethod
    def loads(
        string: Union[bytes, str], obj: bool = False, jsonc: bool = False, **kwargs: Any
    ) -> Any:
        """Parse JSON string/bytes and return raw representation"""
        if obj:
            return jsonify(jsonlib.loads(string, jsonc=jsonc, **kwargs))
        return jsonlib.loads(string, jsonc=jsonc, **kwargs)

    @staticmethod
    def parse(
        string: Union[bytes, str], obj: bool = False, jsonc: bool = False, **kwargs: Any
    ) -> Any:
        """Parse JSON string/bytes"""
        if obj:
            return jsonify(jsonlib.loads(string, jsonc=jsonc, **kwargs))
        return jsonlib.loads(string, jsonc=jsonc, **kwargs)

    @staticmethod
    def orjson_useable() -> bool:
        return jsonlib.orjson_useable()

    @staticmethod
    def rapidjson_useable() -> bool:
        return jsonlib.rapidjson_useable()

    @staticmethod
    def use_orjson() -> None:
        jsonlib.use_orjson()

    @staticmethod
    def use_rapidjson() -> None:
        jsonlib.use_rapidjson()

    @staticmethod
    def use_json_stdlib() -> None:
        jsonlib.use_json_stdlib()

    @staticmethod
    def which() -> str:
        """Return the name of the JSON library being used as a backend"""
        return jsonlib.which()

    @staticmethod
    def json_lib() -> str:
        """Return the name of the JSON library being used as a backend"""
        return jsonlib.which()

    @staticmethod
    def jsonify(value: Any) -> Any:
        """Alias for jsonbourne.core.jsonify"""
        return jsonify(value)

    @staticmethod
    def unjsonify(value: Any) -> Any:
        """Alias for jsonbourne.core.unjsonify"""
        return unjsonify(value)


class JSONModuleCls(ModuleType, JSON):
    @staticmethod
    def __call__(value: Any = None):  # type: ignore[no-untyped-def]
        """Jsonify a value"""
        if value is None:
            return JsonObj()
        return jsonify(value)


@lru_cache(maxsize=None)
def _cls_protected_attrs(cls: Any) -> Set[str]:
    """Return attrs-attribute names for an object decorated with attrs"""
    return set(dir(cls))


stringify = JSON.stringify
parse = JSON.parse

if __name__ == "__main__":
    import doctest

    doctest.testmod()
