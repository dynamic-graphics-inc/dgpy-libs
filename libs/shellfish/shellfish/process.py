# -*- coding: utf-8 -*-
"""Current running process info"""
from __future__ import annotations

import os
import platform
import sys

from os import environ
from typing import Callable, Dict, Iterator, List, Optional, Union, cast

IS_WIN = os.name == "nt"
PYTHON_IMPLEMENTATION = platform.python_implementation()
SYS_PATH_SEP: str = os.pathsep

__all__ = (
    "ENV",
    "Env",
    "PYTHON_IMPLEMENTATION",
    "SYS_PATH_SEP",
    "env",
    "env_dict",
    "is_cpython",
    "is_mac",
    "is_notebook",
    "is_pypy",
    "is_win",
    "is_wsl",
    "ismac",
    "iswin",
    "iswsl",
    "opsys",
    "sys_path_sep",
)

_OS_ENVIRON_ATTRS = set(dir(os.environ))


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
                return cast(Callable[..., str], environ.__getattribute__(item))
        except AttributeError:
            ...
        return cls.__getitem__(item)

    def __setattr__(cls, key: str, value: str) -> None:
        if hasattr(environ, key):
            raise ValueError(f"Key ({key}) is protected; set with __setitem__")
        return cls.__setitem__(key, value)

    update = environ.update
    get = environ.get
    setdefault = environ.setdefault
    clear = environ.clear
    items = environ.items
    keys = environ.keys

    def asdict(cls) -> Dict[str, str]:
        return {k: v for k, v in environ.items()}


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
        >>> {k: v for k, v in Env.items() if k == 'SOMEENVVARIABLE'}
        {'SOMEENVVARIABLE': 'value'}

    """

    ...


env = ENV = Env


def env_dict() -> Dict[str, str]:
    """Return the current enviroment as a dictionary"""
    return env.asdict()


def is_mac() -> bool:
    """Determine if current operating system is macos/osx

    Returns:
        True if on a mac; False otherwise

    """
    return "darwin" in platform.system().lower()


def is_win() -> bool:
    """Determine if current operating system is windows

    Returns:
        True if on a windows machine; False otherwise

    """
    return IS_WIN


def is_wsl() -> bool:
    """Return True if python is running under (WSL); Return False otherwise"""
    if sys.platform in {"win32", "cygwin", "darwin"}:
        return False

    if "microsoft" in platform.release().lower():
        return True

    try:
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                return True
    except FileNotFoundError:
        pass

    return False


def is_notebook() -> bool:
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
    return "lin"


def hostname() -> str:
    """Return the current computer's hostname"""
    return platform.node()


def sys_path_sep() -> str:
    """Return the system path separator string (; on windows -- : otherwise)"""
    return os.pathsep


def syspath_paths(syspath: Optional[str] = None) -> List[str]:
    """Return the current sys.path as a list"""
    if syspath is None:
        return list(filter(None, sys.path))
    return list(filter(None, syspath.split(os.pathsep)))


ismac = is_mac
iswin = is_win
iswsl = is_wsl
