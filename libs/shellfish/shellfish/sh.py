# -*- coding: utf-8 -*-
"""shell utils"""
from functools import lru_cache
from os import (
    chdir,
    chmod as _chmod,
    environ,
    getcwd,
    makedirs,
    mkdir as _mkdir,
    path,
    utime,
)
from shlex import split as _shplit
from shutil import which as _which

from xtyping import IO, Any, FsPath, List, Optional

__all__ = (
    'Flag',
    'cd',
    'echo',
    'export',
    'setenv',
    'which',
    'where',
)


class _FlagMeta(type):
    """Meta class"""

    @staticmethod
    @lru_cache(maxsize=None)
    def attr2flag(string: str) -> str:
        """Convert and return attr to string"""
        return string.replace('_', '-')

    def __getattr__(self, name: str) -> str:
        return self.attr2flag(string=name)


class Flag(metaclass=_FlagMeta):
    """Flag obj

    Examples:
        >>> Flag.__help
        '--help'
        >>> Flag._v
        '-v'

    """

    ...


#############
## ALIASES ##
#############
def pwd() -> str:
    """Return present-working-directory path string; alias for os.getcwd

    Returns:
        str: present working directory as string

    """
    return getcwd()


def dirname(fspath: FsPath) -> str:
    """Return dirname/parent-dir of given path; alias of os.path.dirname

    Args:
        fspath: File-system path

    Returns:
        str: basename of path

    """
    return path.dirname(str(fspath))


def basename(fspath: FsPath) -> str:
    """Return the basename of given path; alias of os.path.dirname

    Args:
        fspath: File-system path

    Returns:
        str: basename of path

    """
    return path.basename(str(fspath))


def cd(dirpath: FsPath) -> None:
    """Change directory to given dirpath; alias for `os.chdir`

    Args:
        dirpath: Directory fspath

    """
    chdir(str(dirpath))


def chmod(fspath: FsPath, mode: int) -> None:
    """Change the access permissions of a file

    Args:
        fspath (FsPath): Path to file to chmod
        mode (int): Permissions mode as an int

    """
    return _chmod(path=str(fspath), mode=mode)


def echo(
    *args: Any, sep: str = ' ', end: str = '\n', file: Optional[IO[Any]] = None
) -> None:
    """Print/echo function

    Args:
        *args: Item(s) to print/echo
        sep: Separator to print with
        end: End of print suffix; defaults to `\n`
        file: File like object to write to if not stdout

    """
    print(*args, sep=sep, end=end, file=file)  # noqa: T001


def export(key: str, val: Optional[str] = None) -> None:
    """Export/Set an environment variable

    Args:
        key (str): environment variable name/key
        val (str): environment variable value

    """
    if val:
        environ[key] = val
        return
    if "=" in key:
        _key = key.split("=")[0]
        return export(_key, key[len(_key) + 1 :])
    raise ValueError(
        f'Unable to parse env variable - key: {str(key)}, value: {str(val)}'
    )


def mkdir(fspath: FsPath, *, p: bool = False, exist_ok: bool = False) -> None:
    """Make directory at given fspath

    Args:
        fspath (FsPath): Directory path to create
        p (bool): Make parent dirs if True; do not make parent dirs if False
        exist_ok (bool): Throw error if directory exists and exist_ok is False

    """
    if p or exist_ok:
        return makedirs(str(fspath), exist_ok=p or exist_ok)
    return _mkdir(str(fspath))


def mkdirp(fspath: FsPath) -> None:
    """Make directory and parents"""
    return mkdir(fspath=fspath, p=True)


def setenv(key: str, val: Optional[str] = None) -> None:
    """Export/Set an environment variable

    Args:
        key (str): environment variable name/key
        val (str): environment variable value

    """
    return export(key=key, val=val)


def touch(fspath: FsPath) -> None:
    """Create an empty file given a fspath

    Args:
        fspath (FsPath): File-system path for where to make an empty file

    """
    if not path.exists(str(fspath)):
        makedirs(path.dirname(str(fspath)), exist_ok=True)
        with open(fspath, "a"):
            utime(fspath, None)


def shplit(string: str, comments: bool = False, posix: bool = True) -> List[str]:
    """Typed alias for shlex.split"""
    return _shplit(string, comments=comments, posix=posix)


def which(cmd: str, path: Optional[str] = None) -> Optional[str]:
    """Return the result of `shutil.which`

    Args:
        cmd (str): Command/exe to find path of
        path (str): System path to use

    Returns:
        Optional[str]: path to command/exe

    """
    return _which(cmd, path=path)


def where(cmd: str, path: Optional[str] = None) -> Optional[str]:
    """Return the result of `shutil.which`; alias of shellfish.sh.which

    Args:
        cmd (str): Command/exe to find path of
        path (str): System path to use

    Returns:
        Optional[str]: path to command/exe

    """
    return which(cmd, path=path)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
