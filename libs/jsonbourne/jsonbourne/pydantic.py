# -*- coding: utf-8 -*-
"""JSONBourne + Pydantic"""

from functools import lru_cache
from pprint import pformat
from typing import Any, Dict, Set

from pydantic import BaseConfig, BaseModel, Extra, Field, ValidationError

from jsonbourne.core import JSON, JsonObj


__all__ = [
    'JsonBaseModelDefaultConfig',
    'JsonBaseModel',
    'BaseModel',
    'Field',
    'ValidationError',
]


class JsonBaseModelDefaultConfig(BaseConfig):
    """Pydantic model config class for JsonBaseModel; can be overridden"""

    # Sometimes hypothesis breaks and will try to add an attribute to
    # objects while testing. Ya can check for 'pytest' if hypothesis breaks
    # (which it sometimes does) with `'pytest' in sys.modules`
    extra = Extra.forbid  # Forbid extras as strictness is good w/ python
    arbitrary_types_allowed = True  # Allow
    allow_population_by_field_name = True
    json_loads = JSON.loads
    json_dumps = JSON.dumps


class JsonBaseModel(BaseModel, JsonObj):  # type: ignore
    """Hybrid `pydantic.BaseModel` and `jsonbourne.JsonObj`"""

    Config = JsonBaseModelDefaultConfig

    def __init__(self, *args: Any, **kwargs: Any):  # type: ignore
        """Construct a JsonBaseModel and allow for `__post_init__` functions"""
        super().__init__(*args, **kwargs)
        self.__post_init__()

    def __post_init__(self) -> Any:
        """Function place holder that is called after object initialization"""
        pass  # pylint: disable=unnecessary-pass

    def to_str(
        self, minify: bool = False, width: int = 120, fmt_kwargs: bool = False
    ) -> str:
        if fmt_kwargs:
            return type(self).__name__ + "(" + self.__repr_str__(", ") + ")"
        if minify:
            return type(self).__name__ + "(**" + str(self.to_dict_filter_none()) + ")"
        return "".join(
            [
                type(self).__name__,
                "(**{\n     ",
                pformat(self.to_dict_filter_none(), width=width)[1:-1].replace(
                    "\n", "\n    "
                ),
                "\n})",
            ]
        )

    def __repr__(self) -> str:
        return self.to_str(fmt_kwargs=True)

    def __str__(self) -> str:
        return self.to_str(minify=False)

    def _repr_html_(self) -> str:
        """Return the HTML representation of the object"""
        return "<pre>{}</pre>".format(self.__str__())

    def to_dict_filter_none(self) -> Dict[str, Any]:
        """Eject object and filter key-values equal to (sub)class' default

        Examples:
            >>> from typing import Optional
            >>> class Thing(JsonBaseModel):
            ...     a: int = 1
            ...     b: str = "herm"
            ...     c: Optional[str] = None
            ...
            >>> t = Thing()
            >>> t
            Thing(a=1, b='herm', c=None)
            >>> t.to_dict_filter_none()
            {'a': 1, 'b': 'herm'}
            >>> t.to_json_obj_filter_none()
            JsonObj(**{'a': 1, 'b': 'herm'})

        """
        return {k: v for k, v in self.dict().items() if v is not None}

    def to_dict_filter_defaults(self) -> Dict[str, Any]:
        """Eject object and filter key-values equal to (sub)class' default

        Examples:
            >>> class Thing(JsonBaseModel):
            ...     a: int = 1
            ...     b: str = "herm"
            ...
            >>> t = Thing()
            >>> t
            Thing(a=1, b='herm')
            >>> t.to_dict_filter_defaults()
            {}
            >>> t.to_json_obj_filter_defaults()
            JsonObj(**{})
            >>> t = Thing(a=123)
            >>> t
            Thing(a=123, b='herm')
            >>> t.to_dict_filter_defaults()
            {'a': 123}
            >>> t.to_json_obj_filter_defaults()
            JsonObj(**{'a': 123})

        """
        defaults = self.defaults_dict()
        return {
            k: v
            for k, v in self.dict().items()
            if k not in defaults or v != defaults[k]
        }

    def to_json_obj_filter_defaults(self) -> JsonObj:
        """Eject to JsonObj and filter key-values equal to (sub)class' default"""
        return JsonObj(self.to_dict_filter_defaults())

    def to_json_obj_filter_none(self) -> JsonObj:
        """Eject to JsonObj and filter key-values where the value is None"""
        return JsonObj(self.to_dict_filter_none())

    def to_json_dict(self) -> JsonObj:
        """Eject object and sub-objects to `jsonbourne.JsonObj`

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
        return JsonObj(
            {
                k: v if not isinstance(v, JsonBaseModel) else v.to_json_dict()
                for k, v in self.__dict__.items()
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        """Eject and return object as plain jane dictionary"""
        return self.eject()

    @classmethod
    def from_dict_filtered(cls, dictionary: Dict[str, Any]) -> "JsonBaseModel":
        """Create class from dict filtering keys not in (sub)class' fields"""
        attr_names: Set[str] = set(cls._cls_field_names())
        return cls(**{k: v for k, v in dictionary.items() if k in attr_names})

    @classmethod
    def has_required_fields(cls) -> bool:
        """Return True/False if the (sub)class has any fields that are required

        Returns:
            bool: True if any fields for a (sub)class are required

        """
        return any(val.required for val in cls.__fields__.values())

    def is_default(self) -> bool:
        """"""
        if self.has_required_fields():
            return False
        return all(
            mfield.default == self[fname] for fname, mfield in self.__fields__.items()
        )

    def __delattr__(self, item: str) -> Any:
        if item in self.__private_attributes__:
            return object.__delattr__(self, item)
        return super().__delattr__(item)

    def __getattr__(self, item: str) -> Any:
        if item in self.__private_attributes__:
            return object.__getattribute__(self, item)
        return super().__getattr__(item)

    @classmethod
    def defaults_dict(cls) -> Dict[str, Any]:
        """Return a dictionary of non-required keys -> default value(s)

        Returns:
            Dict[str, Any]: Dictionary of non-required keys -> default value

        Examples:
            >>> class Thing(JsonBaseModel):
            ...     a: int = 1
            ...     b: str = "herm"
            ...
            >>> t = Thing()
            >>> t
            Thing(a=1, b='herm')
            >>> t.to_dict_filter_defaults()
            {}
            >>> t.to_json_obj_filter_defaults()
            JsonObj(**{})
            >>> t = Thing(a=123)
            >>> t
            Thing(a=123, b='herm')
            >>> t.to_dict_filter_defaults()
            {'a': 123}
            >>> t.to_json_obj_filter_defaults()
            JsonObj(**{'a': 123})
            >>> t.defaults_dict()
            {'a': 1, 'b': 'herm'}

        """
        return {k: v.default for k, v in cls.__fields__.items() if not v.required}

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__private_attributes__:
            return object.__setattr__(self, name, value)
        elif name in self.__property_fields__:
            property_field = getattr(self.__class__, name)
            property_field.fset(self, value)
        else:
            super().__setattr__(name, value)

    @property
    def __property_fields__(self) -> Set[str]:
        """Returns a set of property names for the class that have a setter"""
        return self.__class__._cls_property_fields()

    @classmethod
    @lru_cache(maxsize=1)
    def _cls_property_fields(cls) -> Set[str]:
        """Return a set of property names with a setter function"""
        return {
            k
            for k, v in ((el, getattr(cls, el)) for el in dir(cls))
            if isinstance(v, property) and v.fset is not None
        }

    @classmethod
    def _cls_field_names(cls) -> Set[str]:
        """Return pydantic field names"""
        return {el for el in cls.__fields__}

    def _field_names(self) -> Set[str]:
        """Return pydantic field names"""
        return self.__class__._cls_field_names()
