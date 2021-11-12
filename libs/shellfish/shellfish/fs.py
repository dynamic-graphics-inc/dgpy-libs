# -*- coding: utf-8 -*-
"""file-system utils"""
from os import DirEntry, fspath as _fspath, path, scandir, stat
from time import time

from xtyping import FsPath, Iterable, List

__all__ = (
    'fspath',
    'scandir_list',
    'is_dir',
    'is_file',
    'is_link',
    'isdir',
    'isfile',
    'islink',
    'filecmp',
    'lbytes_gen',
    'rbytes_gen',
    'file_size',
    'filepath_mtimedelta_sec',
)

fspath = _fspath


def is_file(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return path.isfile(_fspath(fspath))


def is_dir(fspath: FsPath) -> bool:
    """Return True if the given path is a directory; False otherwise"""
    return path.isdir(_fspath(fspath))


def is_link(fspath: FsPath) -> bool:
    """Return True if the given path is a link; False otherwise"""
    return path.islink(_fspath(fspath))


def exists(fspath: FsPath) -> bool:
    """Return True if the given path exists; False otherwise"""
    return path.exists(_fspath(fspath))


isfile = is_file
isdir = is_dir
islink = is_link


def file_size(fspath: FsPath) -> int:
    """Return the size of the given file(path) in bytes

    Args:
        fspath (FsPath): Filepath as a string or pathlib.Path object

    Returns:
        int: size of the fspath in bytes

    """
    return stat(fspath).st_size


def scandir_list(dirpath: FsPath = '.') -> List[DirEntry]:
    """Return a list of os.DirEntry objects

    Args:
        dirpath: Dirpath to scan

    Returns:
        List[DirEntry]: List of os.DirEntry objects

    """
    return list(scandir(_fspath(dirpath)))


def filepath_mtimedelta_sec(filepath: FsPath) -> float:
    """Return the seconds since the file(path) was last modified"""
    return time() - path.getmtime(_fspath(filepath))


def wbytes(
    filepath: FsPath,
    bites: bytes,
    *,
    append: bool = False,
) -> bool:
    """Write/Save bytes to a fspath

    The parameter 'bites' is used instead of 'bytes' so as to not redefine
    the built-in python bytes object.

    Args:
        filepath: fspath to write to
        bites: Bytes to be written
        append (bool): Append to the file if True, overwrite otherwise; default
            is False

    Returns:
        None

    Examples:
        >>> from shellfish.fs import rbytes, wbytes
        >>> fspath = "sbytes.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> wbytes(fspath, bites_to_save)
        True
        >>> rbytes(fspath)
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    _write_mode = "ab" if append else "wb"
    with open(filepath, _write_mode) as fd:
        fd.write(bites)
    return True


def rbytes(filepath: FsPath) -> bytes:
    """Load/Read bytes from a fspath

    Args:
        filepath: fspath read as bytes

    Returns:
        bytes from the fspath

    Examples:
        >>> from shellfish.fs import rbytes, wbytes
        >>> fspath = "lbytes.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> wbytes(fspath, bites_to_save)
        True
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> rbytes(fspath)
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    with open(filepath, "rb") as file:
        return bytes(file.read())


def rbytes_gen(filepath: FsPath, blocksize: int = 65536) -> Iterable[bytes]:
    """Yield bytes from a given fspath"""
    with open(filepath, "rb") as f:
        while True:
            data = f.read(blocksize)
            if not data:
                break
            yield data


def rstring(filepath: FsPath) -> str:
    r"""Load/Read a string given a fspath

    Args:
        filepath: Filepath for file to read

    Returns:
        str: String read from given fspath

    Examples:
        ``` python
        >>> from shellfish.fs import rstring, wstring
        >>> fspath = "lstring.doctest.txt"
        >>> sstring(fspath, r'Check out this string')
        >>> lstring(fspath)
        'Check out this string'
        >>> import os; os.remove(fspath)

        ```

    """
    _bytes = rbytes(filepath=filepath)
    try:
        return _bytes.decode(encoding="utf-8")
    except UnicodeDecodeError:  # Catch the unicode decode error
        pass
    return _bytes.decode(encoding="latin2")


def wstring(
    filepath: FsPath,
    string: str,
    *,
    encoding: str = "utf-8",
    append: bool = False,
) -> None:
    """Save/Write a string to fspath

    Args:
        filepath: fspath to write to
        string (str): string to be written
        encoding: String encoding to write file with
        append (bool): Flag to append to file; default = False

    Returns:
        None

    Examples:
        >>> from shellfish.fs import rstring, wstring
        >>> fspath = "sstring.doctest.txt"
        >>> wstring(fspath, r'Check out this string')
        >>> rstring(fspath)
        'Check out this string'
        >>> import os; os.remove(fspath)

    """
    sbytes(
        filepath=filepath,
        bites=string.encode(encoding),
        append=append,
    )


def filecmp(
    left: FsPath, right: FsPath, *, shallow: bool = True, blocksize: int = 65536
) -> bool:
    """Compare 2 files for equality given their filepaths

    Args:
        left (FsPath): Filepath 1
        right (FsPath): Filepath 2
        shallow (bool): Check only size and modification time if True
        blocksize (int): Chunk size to read files

    Returns:
        True if files are equal, False otherwise

    """
    left_stat = stat(left)
    right_stat = stat(right)
    if (
        shallow
        and left_stat.st_size == right_stat.st_size
        and left_stat.st_mtime == right_stat.st_mtime
    ):
        return True
    if left_stat.st_size != right_stat.st_size:
        return False
    return not any(
        left_chunk != right_chunk
        for left_chunk, right_chunk in zip(
            rbytes_gen(left, blocksize=blocksize),
            rbytes_gen(right, blocksize=blocksize),
        )
    )


# IO function aliases
lbytes = rbytes
sbytes = wbytes
lstring = rstring
sstring = wstring
lbytes_gen = rbytes_gen

if __name__ == "__main__":
    from doctest import testmod

    testmod()
