# -*- coding: utf-8 -*-
"""Core for requires"""
import asyncio
import sys

from dataclasses import dataclass
from functools import wraps
from importlib import import_module
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union


T = TypeVar("T")


def _fn_globals(f: Any) -> Any:
    if hasattr(f, "__wrapped__"):
        return _fn_globals(f.__wrapped__)
    return f.__globals__


class RequirementError(ModuleNotFoundError):
    """Exception for requries"""

    pass


class RequirementAttributeError(AttributeError):
    """Requirement attribute error"""

    pass


@dataclass
class Requirement:
    _import: str
    _from: Optional[str] = None
    _as: Optional[str] = None
    pip: Optional[Union[str, bool]] = None
    conda: Optional[Union[str, bool]] = None
    conda_forge: Optional[Union[str, bool]] = None
    details: Optional[Union[str, List[str]]] = None

    def __post_init__(self) -> None:
        pass

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
            return ''
        return (
            self.details if isinstance(self.details, str) else '\n'.join(self.details)
        )

    def err(self) -> RequirementError:
        _install_str = [
            f"    {el}"
            for el in filter(
                None,
                [
                    self._pip_install_str(),
                    self._conda_install_str() if self.conda else None,
                    self._conda_forge_install_str() if self.conda_forge else None,
                    self._details_str() if self.details is not None else None,
                ],
            )
        ]
        msg_parts = [
            f"Module/Package(s) not found/installed; could not import: `{self.import_string}`",
            *_install_str,
        ]
        return RequirementError("\n".join(msg_parts))

    def error(self) -> RequirementError:
        return self.err()

    def raise_error(self) -> None:
        raise self.err()

    def __proxy__(self) -> 'RequirementProxy':
        return RequirementProxy(req=self)

    def proxy(self) -> 'RequirementProxy':
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
                )
        except ModuleNotFoundError:
            return RequirementProxy(req=self)

    @property
    def __requirement__(self) -> Any:
        return self.import_requirement()

    @property
    def alias(self) -> str:
        return self._as or self._import

    def __call__(self, f: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(f) or asyncio.iscoroutine(f):

            @wraps(f)
            async def _requires_dec_async(*args: Any, **kwargs: Any) -> T:
                try:
                    return await f(*args, **kwargs)  # type: ignore
                except NameError as ne:
                    if self.alias not in parse_name_error(ne):
                        raise ne
                except TypeError:
                    pass
                try:
                    _f_globals = _fn_globals(f)
                    if self.alias not in _f_globals:
                        _f_globals[self.alias] = self.import_requirement()
                    retval = await f(*args, **kwargs)  # type: ignore
                    return retval
                except ModuleNotFoundError:
                    tb = sys.exc_info()[2]
                    raise self.err().with_traceback(tb)

            return _requires_dec_async  # type: ignore

        @wraps(f)
        def _requires_dec(*args: Any, **kwargs: Any) -> T:
            try:
                return f(*args, **kwargs)
            except NameError as ne:
                if self.alias not in parse_name_error(ne):
                    raise ne
            except TypeError:
                pass

            try:
                _f_globals = _fn_globals(f)
                if self.alias not in _f_globals:
                    _f_globals[self.alias] = self.import_requirement()
                retval = f(*args, **kwargs)
                return retval
            except ModuleNotFoundError:
                tb = sys.exc_info()[2]
                raise self.err().with_traceback(tb)

        return _requires_dec


class RequirementProxy:
    req: Requirement

    def __init__(self, req: Requirement) -> None:
        self.req = req

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        tb = sys.exc_info()[1]
        raise self.req.err().with_traceback(tb)  # type: ignore

    def __getattr__(self, item: str) -> Any:
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            pass
        return RequirementProxy(req=self.req)


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
    return [el.split(" ")[1].strip(("'")) for el in ne.args]


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
    requirement: Union[str, Requirement, Dict[str, str]]
) -> Requirement:
    if isinstance(requirement, Requirement):
        return requirement
    elif isinstance(requirement, str):
        return string2requirement(string=requirement)
    elif isinstance(requirement, dict):
        if "import" in requirement:
            requirement["_import"] = requirement.pop("import")
        if "from" in requirement:
            requirement["_from"] = requirement.pop("from")
        if "as" in requirement:
            requirement["_as"] = requirement.pop("as")
        return Requirement(**requirement)
    raise RequirementError(
        "Unable to create requirement (type: {}): {}".format(
            str(type(requirement)), str(requirement)
        )
    )


def make_requirements(
    requirements: Union[
        List[Union[str, Requirement, Dict[str, str]]],
        Tuple[Union[str, Requirement, Dict[str, str]]],
    ]
) -> List[Requirement]:
    if isinstance(requirements, (list, tuple)):
        return [make_requirement(req) for req in requirements]
    return make_requirements([requirements])


def require(*args: Any, **kwargs: Any) -> Requirement:
    return Requirement(*args, **kwargs)


def requires(
    *requirements: Union[str, Dict[str, str], Requirement],
    _import: Optional[str] = None,
    _as: Optional[str] = None,
    _from: Optional[str] = None,
    pip: Optional[Union[str, bool]] = None,
    conda: Optional[Union[str, bool]] = None,
    conda_forge: Optional[Union[str, bool]] = None,
    details: Optional[str] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to specify the packages a function or class requires

    The decorator will not do anything unless a NameError is thrown. If a
    NameError is thrown then the required package is likely not installed and
    a `RequirementError` will be thrown with instructions on how to install
    the required packages.

    Args:
        *requirements: Any number of required package names as strings

    Returns:
        Function wrapped such that in the event of a `NameError` a helpful
        error is raised.

    """
    _kwargs = (_import, _from, _as, pip, conda, conda_forge)
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
            )
        ]
    else:
        _requirements = make_requirements(list(requirements))

    def _requires_dec(f: Callable[..., T]) -> Callable[..., T]:
        _wrapped_fn = f
        for el in _requirements:
            _wrapped_fn = el(_wrapped_fn)
        wraps(f)(_wrapped_fn)
        return _wrapped_fn

    return _requires_dec


if __name__ == "__main__":
    import doctest

    doctest.testmod()
