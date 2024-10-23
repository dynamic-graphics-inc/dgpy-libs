# -*- coding: utf-8 -*-
"""JSONBourne + Pydantic"""

from __future__ import annotations

from functools import lru_cache
from pprint import pformat
from shutil import get_terminal_size
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    MutableMapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from pydantic import (  # BaseConfig,; BaseSettings,
    VERSION as __pydantic_version__,
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
)
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated, TypeGuard

from jsonbourne.core import JSON, JsonObj

T = TypeVar("T")
JsonBaseModelT = TypeVar("JsonBaseModelT", bound="JsonBaseModel")

__all__ = (
    "BaseModel",
    "Field",
    "JsonBaseConfig",
    "JsonBaseModel",
    "JsonBaseModelDefaultConfig",
    "JsonBaseModelT",
    "ValidationError",
    # pydantic
    "__pydantic_version__",
)

json_model_base_config: ConfigDict = {
    "extra": "forbid",
    "arbitrary_types_allowed": True,
    "populate_by_name": True,
    "use_enum_values": True,
    "validate_default": True,
}


class JsonBaseConfig:
    """Pydantic v1 model config class for JsonBaseModel; can be overridden"""

    # Sometimes hypothesis breaks and will try to add an attribute to
    # objects while testing. Ya can check for 'pytest' if hypothesis breaks
    # (which it sometimes does) with `'pytest' in sys.modules`
    extra = "forbid"  # Forbid extras as strictness is good w/ python
    arbitrary_types_allowed = True  # Allow
    allow_population_by_field_name = True
    json_loads = JSON.loads
    json_dumps = JSON.dumps
    use_enum_values = True


class JsonBaseModelDefaultConfig(JsonBaseConfig): ...


def is_json_obj_like(v: Any) -> TypeGuard[Union[JsonObj[Any], Dict[str, Any]]]:
    return isinstance(v, (JsonObj, dict))


def json_obj_before_validator(
    v: Union[JsonObj[T], Dict[str, T], Any],
) -> JsonObj[T]:
    if not is_json_obj_like(v):
        raise ValueError(f"Expected JsonObj, got {type(v)}")
    if isinstance(v, JsonObj):
        return v
    return JsonObj(**v)


TJsonObjPydantic = Annotated[JsonObj, BeforeValidator(json_obj_before_validator)]


class JsonBaseModel(BaseModel, JsonObj, MutableMapping):  # type: ignore[type-arg]
    """Hybrid `pydantic.BaseModel` and `jsonbourne.JsonObj`"""

    model_config = json_model_base_config

    def __post_init__(self) -> Any:
        """Function place holder that is called after object initialization"""
        # pylint: disable=unnecessary-pass

    def model_post_init(self, __config: Any) -> None:
        self.__post_init__()

    @property
    def _data(self) -> Dict[str, Any]:  # type: ignore[override]
        return self.__dict__

    def __dumpable__(self) -> Dict[str, Any]:
        return self.model_dump()

    def __json_interface__(self) -> Dict[str, Any]:
        return self.model_dump()

    # ===================================
    # ALIASES (SANS DEPRECATION WARNINGS)
    # ===================================
    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Alias for `model_dump`"""
        return self.model_dump(*args, **kwargs)

    def json(self, *args: Any, **kwargs: Any) -> str:
        """Alias for `model_dumps`"""
        return self.model_dump_json(*args, **kwargs)

    def to_str(
        self,
        minify: bool = False,
        width: Optional[int] = None,
        fmt_kwargs: bool = False,
    ) -> str:
        if fmt_kwargs:
            return type(self).__name__ + "(" + self.__repr_str__(", ") + ")"  # type: ignore[misc]
        if minify:
            return type(self).__name__ + "(**" + str(self.to_dict_filter_none()) + ")"
        _width = width or get_terminal_size((88, 24)).columns - 12
        return "".join(
            [
                type(self).__name__,
                "(**{\n     ",
                pformat(self.to_dict_filter_none(), width=_width)[1:-1].replace(
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
        return f"<pre>{self.__str__()}</pre>"

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
        return {k: v for k, v in self.model_dump().items() if v is not None}

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
            for k, v in self.model_dump().items()
            if k not in defaults or v != defaults[k]
        }

    def to_json_obj_filter_defaults(self) -> JsonObj[Any]:
        """Eject to JsonObj and filter key-values equal to (sub)class' default"""
        return JsonObj(self.to_dict_filter_defaults())

    def to_json_obj_filter_none(self) -> JsonObj[Any]:
        """Eject to JsonObj and filter key-values where the value is None"""
        return JsonObj(self.to_dict_filter_none())

    def to_json_obj(self) -> JsonObj[Any]:
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

    def to_json_dict(self) -> JsonObj[Any]:
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
        return self.to_json_obj()

    def to_dict(self) -> Dict[str, Any]:
        """Eject and return object as plain jane dictionary"""
        return self.eject()

    def JSON(
        self,
        fmt: bool = False,
        pretty: bool = False,
        sort_keys: bool = False,
        append_newline: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
        **kwargs: Any,
    ) -> str:
        return JSON.dumps(
            self.model_dump(),
            fmt=fmt,
            pretty=pretty,
            sort_keys=sort_keys,
            append_newline=append_newline,
            default=default,
            **kwargs,
        )

    @classmethod
    def from_dict_filtered(
        cls: Type[JsonBaseModelT], dictionary: Dict[str, Any]
    ) -> JsonBaseModelT:
        """Create class from dict filtering keys not in (sub)class' fields"""
        attr_names: Set[str] = set(cls._cls_field_names())
        return cls(**{k: v for k, v in dictionary.items() if k in attr_names})

    @classmethod
    def has_required_fields(cls) -> bool:
        """Return True/False if the (sub)class has any fields that are required

        Returns:
            bool: True if any fields for a (sub)class are required

        """
        return any(val.is_required() for val in cls.model_fields.values())

    def is_default(self) -> bool:
        """Check if the object is equal to the default value for its fields

        Returns:
            True if object is equal to the default value for all fields; False otherwise

        Examples:
            >>> class Thing(JsonBaseModel):
            ...    a: int = 1
            ...    b: str = 'b'
            ...
            >>> t = Thing()
            >>> t.is_default()
            True
            >>> t = Thing(a=2)
            >>> t.is_default()
            False

        """
        if self.has_required_fields():
            return False
        return all(
            mfield.default == self[fname] for fname, mfield in self.model_fields.items()
        )

    def __delattr__(self, item: str) -> Any:
        if self.__pydantic_private__ is not None and item in self.__pydantic_private__:
            return object.__delattr__(self, item)
        return super().__delattr__(item)

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:  # type: ignore[override]
        return super().__iter__()

    def __getitem__(self, item: str) -> Any:  # type: ignore[override]
        try:
            return super().__getattr__(item)
        except AttributeError as ae:
            if item in self._data:
                return self._data[item]
            raise ae from None

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
        return {
            k: v.default for k, v in cls.model_fields.items() if not v.is_required()
        }

    def __setattr__(self, name: str, value: Any) -> None:
        return object.__setattr__(self, name, value)

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
        return set(cls.model_fields)

    def _field_names(self) -> Set[str]:
        """Return pydantic field names"""
        return self.__class__._cls_field_names()
