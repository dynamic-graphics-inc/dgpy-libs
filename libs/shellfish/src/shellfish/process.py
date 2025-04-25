# -*- coding: utf-8 -*-
"""Current running process info"""

from __future__ import annotations

import platform
import sys

from contextlib import contextmanager
from os import environ, name as os_name, pathsep
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    ItemsView,
    Iterator,
    KeysView,
    List,
    Optional,
    Type,
    Union,
    ValuesView,
    cast,
)

IS_WIN = os_name == "nt"
PYTHON_IMPLEMENTATION = platform.python_implementation()
SYS_PATH_SEP: str = pathsep

__all__ = (
    "ENV",
    "PYTHON_IMPLEMENTATION",
    "SYS_PATH_SEP",
    "Env",
    "env",
    "env_dict",
    "hostname",
    "is_cpython",
    "is_mac",
    "is_notebook",
    "is_pypy",
    "is_win",
    "is_wsl",
    "ismac",
    "iswin",
    "iswsl",
    "linux_version",
    "opsys",
    "sys_path_sep",
    "syspath_paths",
    "tmpenv",
)
_OS_ENVIRON_ATTRS = set(dir(environ))


@contextmanager
def tmpenv(**kwargs: str) -> Generator[Type[Env], Any, None]:
    """Context manager for Env"""
    old_env = dict(environ)
    if kwargs:
        env.update(kwargs)
    try:
        yield env
    finally:
        environ.clear()
        environ.update(old_env)


class _EnvObjMeta(type):
    def __contains__(cls, key: str) -> bool:
        return key in environ

    def __delitem__(cls, key: str) -> None:
        return environ.__delitem__(key)

    def __getitem__(cls, key: str) -> Optional[str]:
        return environ.get(key)

    def __len__(cls) -> int:
        return len(environ)

    def __iter__(cls) -> Iterator[str]:
        return iter(environ)

    def __setitem__(cls, key: str, value: str) -> None:
        return environ.__setitem__(key, value)

    def __str__(cls) -> str:
        return environ.__str__()[8:-1]

    def __repr__(self) -> str:
        return self.__str__()

    def __getattr__(
        cls, item: str
    ) -> Optional[Union[Callable[[], str], Callable[[str], None], str]]:
        try:
            if item in _OS_ENVIRON_ATTRS:
                return cast("Callable[..., str]", environ.__getattribute__(item))
        except AttributeError:
            ...
        return cls.__getitem__(item)

    def __setattr__(cls, key: str, value: str) -> None:
        if hasattr(environ, key):
            raise ValueError(f"Key ({key}) is protected; set with __setitem__")
        return cls.__setitem__(key, value)

    def update(self, d: Dict[str, str]) -> None:
        return environ.update(d)

    def update_from_dict(self, d: Dict[str, str]) -> None:
        return self.update(d)

    def get(self, key: str, default: Optional[str] = None) -> str:
        if default is None:
            return environ[key]
        return environ.get(key, default)

    def setdefault(self, key: str, default: str) -> str:
        return environ.setdefault(key, default)

    def clear(self) -> None:
        return environ.clear()

    def keys(self) -> KeysView[str]:
        return environ.keys()

    def values(self) -> ValuesView[str]:
        return environ.values()

    def items(self) -> ItemsView[str, str]:
        return environ.items()

    def asdict(cls) -> Dict[str, str]:
        return dict(environ.items())


class Env(metaclass=_EnvObjMeta):
    """Env with attr access

    Examples:
        >>> from os import environ
        >>> if 'SOMEENVVARIABLE' in environ:
        ...     del environ['SOMEENVVARIABLE']
        >>> environ.get('SOMEENVVARIABLE')  # Does not exist in environ
        >>> Env.SOMEENVVARIABLE
        >>> Env.SOMEENVVARIABLE = 'value'
        >>> Env.SOMEENVVARIABLE
        'value'
        >>> environ.get('SOMEENVVARIABLE')
        'value'
        >>> environ['SOMEENVVARIABLE']
        'value'
        >>> 'SOMEENVVARIABLE' in Env
        True
        >>> {k: v for k, v in Env.items() if k == 'SOMEENVVARIABLE'}
        {'SOMEENVVARIABLE': 'value'}
        >>> del Env['SOMEENVVARIABLE']
        >>> 'SOMEENVVARIABLE' in Env
        False

    """


env = ENV = Env


def env_dict() -> Dict[str, str]:
    """Return the current environment-variables as a dictionary"""
    return env.asdict()


def is_mac() -> bool:
    """Determine if current operating system is macos/osx

    Returns:
        True if on a mac; False otherwise

    """
    return "darwin" in platform.system().lower()


def ismac() -> bool:
    """Alias for is_mac()"""
    return is_mac()


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return IS_WIN


def iswin() -> bool:
    """Alias for is_win()"""
    return is_win()


def is_wsl() -> bool:  # pragma: nocov
    """Return True if python is running under (WSL); Return False otherwise"""
    if sys.platform in {"win32", "cygwin", "darwin"}:
        return False

    if "microsoft" in platform.release().lower():
        return True

    try:
        with open("/proc/version") as f:
            if "microsoft" in f.read().lower():
                return True
    except FileNotFoundError:
        pass

    return False


def iswsl() -> bool:
    """Alias for is_wsl()"""
    return is_wsl()


def is_notebook() -> bool:  # pragma: nocov
    """Determine if running in ipython/jupyter notebook; returns True/False"""
    try:
        shell = get_ipython().__class__.__name__  # type: ignore[name-defined]
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def is_pypy() -> bool:
    """Return True if running on pypy3; False otherwise"""
    return "pypy" in platform.python_implementation().lower()


def is_cpython() -> bool:
    """Return True if running on CPython; False otherwise"""
    return "cpython" in platform.python_implementation().lower()


def opsys() -> str:
    """Return the current process' os type: 'mac' | 'lin' | 'win' | 'wsl'"""
    if is_win():
        return "win"
    if is_wsl():
        return "wsl"
    if is_mac():
        return "mac"
    return linux_version()


def linux_version() -> str:
    """Return rhel7 or rhel8 based on the current linux version"""
    try:
        with open("/etc/redhat-release") as file:
            release_info = file.read()
            if "release 7" in release_info:
                return "rhel7"
            elif "release 8" in release_info:
                return "rhel8"
            else:
                return "other"
    except FileNotFoundError:
        return "linux"


def hostname() -> str:
    """Return the current computer's hostname

    Returns:
        str: hostname

    Examples:
        >>> hn = hostname()
        >>> isinstance(hn, str)
        True

    """
    return platform.node()


def sys_path_sep() -> str:
    """Return the system path separator string (; on windows -- : otherwise)

    Examples:
        >>> import os
        >>> sep = sys_path_sep()
        >>> isinstance(sep, str)
        True
        >>> os.pathsep == sep
        True

    """
    return pathsep


def syspath_paths(syspath: Optional[str] = None) -> List[str]:
    """Return the current sys.path as a list

    Examples:
        >>> sys_paths = syspath_paths()
        >>> isinstance(sys_paths, list)
        True
        >>> sys_path_arg = 'path1;path2;path3' if is_win() else 'path1:path2:path3'
        >>> sys_paths_w_args = syspath_paths(syspath=sys_path_arg)
        >>> isinstance(sys_paths_w_args, list)
        True
        >>> sys_paths_w_args == ['path1', 'path2', 'path3']
        True

    """
    if syspath is None:
        return list(filter(None, sys.path))
    return list(filter(None, syspath.split(pathsep)))
