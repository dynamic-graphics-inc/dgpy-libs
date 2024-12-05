# -*- coding: utf-8 -*-
"""Core for requires"""

from __future__ import annotations

import asyncio
import logging
import sys
import warnings

from dataclasses import dataclass, field
from functools import wraps
from importlib import import_module
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)

from xtyping import ParamSpec

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")

__sys_version_info__ = sys.version_info
log = logging.getLogger(__name__)


def _fn_globals(f: Any) -> Any:
    if hasattr(f, "__wrapped__"):
        return _fn_globals(f.__wrapped__)
    return f.__globals__


class RequirementWarning(UserWarning):
    """Warning for requires"""


class RequirementError(ModuleNotFoundError):
    """Exception for requires"""


class RequirementsError(ModuleNotFoundError):
    """Exception for multiple requirements"""


class RequirementAttributeError(AttributeError):
    """Requirement attribute error"""


class RequirementDict(TypedDict):
    """Requirement dict"""

    _import: str
    _from: Optional[str]
    _as: Optional[str]
    pip: Optional[Union[str, bool]]
    conda: Optional[Union[str, bool]]
    conda_forge: Optional[Union[str, bool]]
    details: Optional[Union[str, List[str]]]
    lazy: Optional[bool]  # default true


TRequirementDict = Union[RequirementDict, Dict[str, Any]]


@dataclass(frozen=True, unsafe_hash=True)
class Requirement:
    _import: str
    _from: Optional[str] = None
    _as: Optional[str] = None
    pip: Optional[Union[str, bool]] = None
    conda: Optional[Union[str, bool]] = None
    conda_forge: Optional[Union[str, bool]] = None
    details: Optional[Union[str, List[str]]] = None
    lazy: bool = field(default=True)

    def __post_init__(self) -> None: ...

    def to_dict(self) -> RequirementDict:
        return {
            "_import": self._import,
            "_from": self._from,
            "_as": self._as,
            "pip": self.pip,
            "conda": self.conda,
            "conda_forge": self.conda_forge,
            "details": self.details,
            "lazy": self.lazy,
        }

    @classmethod
    def from_dict(cls, req_dict: RequirementDict) -> Requirement:
        return cls(
            _import=req_dict["_import"],
            _from=req_dict["_from"],
            _as=req_dict["_as"],
            pip=req_dict["pip"],
            conda=req_dict["conda"],
            conda_forge=req_dict["conda_forge"],
            details=req_dict["details"],
            lazy=req_dict.get("lazy", True) or True,
        )

    @property
    def pkg_basename(self) -> str:
        if self._from:
            if "." in self._from:
                return self._from.split(".")[0]
            return self._from

        if "." in self._import:
            return self._import.split(".")[0]
        return self._import

    @property
    def import_string(self) -> str:
        if self._from and self._as:
            return f"from {self._from} import {self._import} as {self._as}"
        elif self._as:
            return f"import {self._import} as {self._as}"
        elif self._from:
            return f"from {self._from} import {self._import}"
        return f"import {self._import}"

    def _pip_install_str(self) -> str:
        if self.pip:
            if isinstance(self.pip, str):
                return f"pip install {self.pip}"
            return f"pip install {self.pkg_basename}"
        return f"pip install {self.pkg_basename} (pip install info unspecified)"

    def _conda_install_str(self) -> str:
        if self.conda:
            if isinstance(self.conda, str):
                return f"conda install {self.conda}"
            return f"conda install {self.pkg_basename}"
        return f"conda install {self.pkg_basename} (conda install info unspecified)"

    def _conda_forge_install_str(self) -> str:
        if self.conda_forge:
            if isinstance(self.conda_forge, str):
                return f"conda install -c conda-forge {self.conda_forge}"
            return f"conda install -c conda-forge {self.pkg_basename}"
        return f"conda install -c conda-forge {self.pkg_basename} (conda-forge install info unspecified)"

    def _details_str(self) -> str:
        if self.details is None:
            return ""
        if isinstance(self.details, str):
            return self.details
        return "\n".join(self.details)

    def err_msg(self) -> str:
        msg_parts = [
            f"Module/Package(s) not found/installed; could not import: `{self.import_string}`",
            *(
                f"    {el}"
                for el in filter(
                    None,
                    [
                        self._pip_install_str(),
                        self._conda_install_str() if self.conda else None,
                        self._conda_forge_install_str() if self.conda_forge else None,
                        self._details_str(),
                    ],
                )
            ),
        ]
        return "\n".join(msg_parts)

    def warning(self) -> RequirementWarning:
        return RequirementWarning(self.err_msg())

    def err(self) -> RequirementError:
        return RequirementError(self.err_msg())

    def error(self) -> RequirementError:
        return self.err()

    def raise_error(self) -> None:
        raise self.err()

    def __proxy__(self) -> "RequirementProxy":
        return RequirementProxy(req=self)

    def proxy(self) -> "RequirementProxy":
        return self.__proxy__()

    def import_requirement(self) -> Any:
        """Import and return the requirement"""
        try:
            if self._from is None:
                return import_module(self._import)
            req = import_module(self._from)
            # Import ok BUT the attr/thing imported from the module does not exist
            try:
                return getattr(req, self._import)
            except AttributeError as ae:
                raise RequirementAttributeError(
                    "\n".join(
                        [
                            f"Module/Package(s) import AttributeError: `{self.import_string}`",
                            f"    AttributeError: {str(ae)}",
                        ]
                    )
                ) from ae
        except ModuleNotFoundError:
            return RequirementProxy(req=self)

    @property
    def __requirement__(self) -> Any:
        return self.import_requirement()

    @property
    def alias(self) -> str:
        return self._as or self._import

    def __call__(self, f: Callable[P, R]) -> Callable[P, R]:
        _f_globals = _fn_globals(f)
        if not self.lazy:
            # Eagerly import the requirement
            try:
                if self.alias not in _f_globals:
                    _f_globals[self.alias] = self.import_requirement()
            except ModuleNotFoundError as mnfe:
                tb = sys.exc_info()[2]
                raise self.err().with_traceback(tb) from mnfe

        if asyncio.iscoroutinefunction(f) or asyncio.iscoroutine(f):

            async def _requires_dec_async(*args: P.args, **kwargs: P.kwargs) -> Any:
                if self.lazy:
                    # Lazy loading logic
                    try:
                        return await f(*args, **kwargs)
                    except NameError as ne:
                        if self.alias not in parse_name_error(ne):
                            raise ne
                    except TypeError:
                        pass
                    try:
                        if self.alias not in _f_globals:
                            _f_globals[self.alias] = self.import_requirement()
                        return await f(*args, **kwargs)
                    except ModuleNotFoundError as mnfe:
                        tb = sys.exc_info()[2]
                        raise self.err().with_traceback(tb) from mnfe
                else:
                    # Eager loading logic
                    try:
                        return await f(*args, **kwargs)
                    except ModuleNotFoundError as mnfe:
                        tb = sys.exc_info()[2]
                        raise self.err().with_traceback(tb) from mnfe

            return _requires_dec_async  # type: ignore[return-value]

        @wraps(f)
        def _requires_dec(*args: P.args, **kwargs: P.kwargs) -> R:
            if self.lazy:
                # lazy loading
                try:
                    return f(*args, **kwargs)
                except NameError as ne:
                    if self.alias not in parse_name_error(ne):
                        raise ne from ne
                except TypeError:
                    pass
                try:
                    if self.alias not in _f_globals:
                        _f_globals[self.alias] = self.import_requirement()
                    return f(*args, **kwargs)
                except ModuleNotFoundError as mnfe:
                    tb = sys.exc_info()[2]
                    raise self.err().with_traceback(tb) from mnfe
            else:
                # eager loading
                try:
                    return f(*args, **kwargs)
                except ModuleNotFoundError as mnfe:
                    tb = sys.exc_info()[2]
                    raise self.err().with_traceback(tb) from mnfe

        # get and/or set the __requires__ attribute
        if hasattr(f, "__requires__"):
            f.__requires__.add(self)
        else:
            f.__requires__ = RequirementsMeta(requirements={self})  # type: ignore[attr-defined]
        return _requires_dec


@dataclass
class RequirementsMeta:
    requirements: Set[Requirement] = field(default_factory=set)

    def __post_init__(self) -> None: ...

    def add(self, requirement: Requirement) -> bool:
        if requirement not in self.requirements:
            self.requirements.add(requirement)
            return True
        return False

    def update(self, requirements: Iterable[Requirement]) -> None:
        self.requirements.update(requirements)

    def remove(self, requirement: Requirement) -> bool:
        if requirement in self.requirements:
            self.requirements.remove(requirement)
            return True
        return False

    def preflight_check(
        self,
        *,
        warn: bool = False,
        on_missing: Optional[Callable[[Set[Requirement]], None]],
    ) -> Set[Requirement]:
        """Check if requirements are met

        Args:
            warn (bool): If True, issues warnings for missing requirements.
            on_missing (Optional[Callable[[Set[Requirement]], None]]): Callback to do something on missing requirements.

        Returns:
            Set[Requirement]: A set of missing requirements

        """
        missing_requirements = {
            prox.req
            for prox in (req.import_requirement() for req in self.requirements)
            if isinstance(prox, RequirementProxy)
        }

        if missing_requirements and on_missing:
            on_missing(missing_requirements)

        if warn and missing_requirements:
            for req in missing_requirements:
                warnings.warn(req.warning(), RequirementWarning, stacklevel=2)

        return missing_requirements


class RequirementProxy:
    req: Requirement

    def __init__(self, req: Requirement) -> None:
        """Create a proxy for a requirement"""
        self.req = req

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Raise the error when the proxy is called as a function"""
        raise self.req.err()

    def __getattr__(self, item: str) -> Any:
        """Raise the error when any attribute is accessed"""
        raise self.req.err()

    def __repr__(self) -> str:
        return f"RequirementProxy({self.req.__repr__()})"

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, key: Any) -> Any:
        """Raise the error when attempting to access items (e.g., proxy[key])"""
        raise self.req.err()

    def __setattr__(self, key: str, value: Any) -> None:
        """Prevent the proxy from being used in attribute assignment"""
        if key == "req":
            object.__setattr__(self, key, value)
        else:
            raise self.req.err()

    def __bool__(self) -> bool:
        """Prevent the proxy from being used in boolean contexts"""
        raise self.req.err()


def parse_name_error(ne: NameError) -> List[str]:
    """Return a list of the missing items specified in a `NameError`

    Args:
        ne (NameError): NameError object

    Returns:
        str: name of the missing thing/pkg/module/function

    Examples:
        >>> args = ("name 'path' is not defined",)
        >>> ne = NameError(*args)
        >>> parse_name_error(ne)
        ['path']

    """
    return [el.split(" ")[1].strip("'") for el in ne.args]


def parse_import_string(string: str) -> Requirement:
    parts = [el for el in string.split(" ") if el]
    parts_set = {*parts}
    if "as" in parts_set and "from" in parts_set:
        _f, _from, _i, _import, _a, _as = parts
        return Requirement(_from=_from, _import=_import, _as=_as)
    elif "from" in parts_set:
        _f, _from, _i, _import = parts
        return Requirement(_from=_from, _import=_import)
    elif "as" in parts_set:
        _i, _import, _a, _as = parts
        return Requirement(_import=_import, _as=_as)
    else:
        _, _import_str = parts
        return Requirement(_import=_import_str)


def string2requirement(string: str) -> Requirement:
    if "import" in string:
        return parse_import_string(string)
    return Requirement(_import=string)


def make_requirement(
    requirement: Union[str, Requirement, TRequirementDict],
) -> Requirement:
    if isinstance(requirement, Requirement):
        return requirement
    elif isinstance(requirement, str):
        return string2requirement(string=requirement)
    elif isinstance(requirement, dict):
        if "import" in requirement:
            requirement["_import"] = requirement.pop("import")  # type: ignore[typeddict-item]
        if "from" in requirement:
            requirement["_from"] = requirement.pop("from")  # type: ignore[typeddict-item]
        if "as" in requirement:
            requirement["_as"] = requirement.pop("as")  # type: ignore[typeddict-item]
        return Requirement(**requirement)

    str_type = str(type(requirement))
    str_req = str(requirement)
    raise RequirementError(
        f"Unable to create requirement (type: {str_type}): {str_req})"
    )


def make_requirements(
    requirements: Union[
        List[Union[str, Requirement, TRequirementDict]],
        Tuple[Union[str, Requirement, TRequirementDict]],
        str,
        Requirement,
        TRequirementDict,
    ],
) -> List[Requirement]:
    if isinstance(requirements, (list, tuple)):
        return [make_requirement(req) for req in requirements]
    return make_requirements([requirements])


def require(*args: Any, **kwargs: Any) -> Requirement:
    return Requirement(*args, **kwargs)


def requires(
    *requirements: Union[str, TRequirementDict, Requirement],
    _import: Optional[str] = None,
    _as: Optional[str] = None,
    _from: Optional[str] = None,
    pip: Optional[Union[str, bool]] = None,
    conda: Optional[Union[str, bool]] = None,
    conda_forge: Optional[Union[str, bool]] = None,
    details: Optional[str] = None,
    lazy: Optional[bool] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to specify the packages a function or class requires

    The decorator will not do anything unless a NameError is thrown. If a
    NameError is thrown then the required package is likely not installed and
    a `RequirementError` will be thrown with instructions on how to install
    the required packages.


    Args:
        *requirements: Any number of required package names as strings
        _import ('str'): `IMPORT` part of `from {FROM} import {IMPORT} as {AS}`
        _as ('str'): `AS` part of `from {FROM} import {IMPORT} as {AS}`
        _from ('str'): `FROM` part of `from {FROM} import {IMPORT} as {AS}`
        pip (Optional[Union[str, bool]]): pip install name
        conda (Optional[Union[str, bool]]): conda install name
        conda_forge (Optional[Union[str, bool]]): conda-forge install name
        details (str): details to be displayed in the error message
        lazy (bool): If True, the requirement is loaded lazily

    Returns:
        Function wrapped such that in the event of a `NameError` a helpful
        error is raised.

    Raises:
        ValueError: If requirements or kwargs are given

    """
    _kwargs = (_import, _from, _as, pip, conda, conda_forge, details, lazy)
    if any(kw for kw in _kwargs):
        if requirements:
            raise ValueError("*requirements and **kwargs are mutually exclusive")
        _requirements = [
            Requirement(
                _import=str(_import),
                _from=_from,
                _as=_as,
                pip=pip,
                conda=conda,
                conda_forge=conda_forge,
                details=details,
                lazy=lazy if lazy is not None else True,
            )
        ]
    else:
        if not requirements:
            raise ValueError("No requirements specified in 'requires' decorator.")
        _requirements = make_requirements(list(requirements))

    def _requires_dec(f: Callable[P, R]) -> Callable[P, R]:
        _wrapped_fn = f
        requirements_meta = RequirementsMeta(requirements=set())
        for el in _requirements:
            _wrapped_fn = el(_wrapped_fn)
            requirements_meta.add(el)
        _wrapped_fn.__requires__ = requirements_meta  # type: ignore[attr-defined]
        wraps(f)(_wrapped_fn)
        return _wrapped_fn

    return _requires_dec


def scope_requirements(debug: bool = False) -> RequirementsMeta:
    """Scan and check calling module scope for objs/fns wrapped with requirements.

    Args:
        debug (bool): If True, log debug info.

    Returns:
        RequirementsMeta: A RequirementsMeta instance with the requirements found during the check.

    """
    calling_frame = sys._getframe(2)
    _f_globals = calling_frame.f_globals
    if debug:
        log.debug(f"calling_frame: {calling_frame}")
        log.debug(f"_f_globals: {_f_globals}")
    scope_reqs = RequirementsMeta(requirements=set())

    for name, obj in _f_globals.items():
        if hasattr(obj, "__requires__"):
            log.debug(f"Found obj with requirements: {name} -> {obj}")
            requirements_meta = obj.__requires__
            if not isinstance(requirements_meta, RequirementsMeta):
                raise RequirementError(
                    f"Expected a RequirementsMeta instance, got {type(requirements_meta)}"
                )
            scope_reqs.update(requirements_meta.requirements)
    return scope_reqs


def preflight_check(
    *,
    warn: bool = False,
    on_missing: Optional[Callable[[Set[Requirement]], None]] = None,
) -> RequirementsMeta:
    """Scan and check calling module scope for objs/fns wrapped with requirements.

    Args:
        warn (bool): If True, issues warnings for missing requirements.
        on_missing (Optional[Callable[[Set[Requirement]], None]]): Callback to do something on missing requirements.

    Returns:
        RequirementsMeta: A RequirementsMeta instance with the requirements found during the check.

    """
    scope_reqs = scope_requirements()
    scope_reqs.preflight_check(warn=warn, on_missing=on_missing)
    return scope_reqs


def requires_python(version: str) -> None:
    """Decorator to specify the python version a function or class requires"""
    raise NotImplementedError("Not yet implemented (TODO)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
