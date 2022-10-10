# -*- coding: utf-8 -*-
"""file-system utils"""
from __future__ import annotations

from enum import IntEnum
from glob import has_magic, iglob
from itertools import chain, count
from os import (
    DirEntry,
    chmod as _chmod,
    fspath as _fspath,
    makedirs as _makedirs,
    mkdir as _mkdir,
    path,
    remove,
    rmdir as _rmdir,
    scandir as _scandir,
    sep,
    stat as _stat,
    stat_result as os_stat_result,
    symlink as _symlink,
    utime,
    walk,
)
from pathlib import Path
from shutil import copytree, move as _move, rmtree
from time import time

from jsonbourne import JSON
from listless import exhaust
from shellfish import const
from shellfish._meta import __version__
from shellfish.fs._async import (
    exists_async as exists_async,
    filesize_async as filesize_async,
    is_dir_async as is_dir_async,
    is_file_async as is_file_async,
    is_link_async as is_link_async,
    isdir_async as isdir_async,
    isfile_async as isfile_async,
    islink_async as islink_async,
    lbytes_async as lbytes_async,
    lbytes_gen_async as lbytes_gen_async,
    ljson_async as ljson_async,
    lstat_async as lstat_async,
    lstr_async as lstr_async,
    lstring_async as lstring_async,
    rbin_async as rbin_async,
    rbin_gen_async as rbin_gen_async,
    rbytes_async as rbytes_async,
    rbytes_gen_async as rbytes_gen_async,
    rjson_async as rjson_async,
    rstr_async as rstr_async,
    rstring_async as rstring_async,
    sbin_async as sbin_async,
    sbytes_async as sbytes_async,
    sbytes_gen_async as sbytes_gen_async,
    sjson_async as sjson_async,
    sstr_async as sstr_async,
    sstring_async as sstring_async,
    stat_async as stat_async,
    wbin_async as wbin_async,
    wbin_gen_async as wbin_gen_async,
    wbytes_async as wbytes_async,
    wbytes_gen_async as wbytes_gen_async,
    wjson_async as wjson_async,
    wstr_async as wstr_async,
    wstring_async as wstring_async,
)
from shellfish.process import is_win
from xtyping import (
    Any,
    AnyStr,
    Callable,
    FsPath,
    Generator,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    cast,
)

# END-IMPORTS


class Stdio(IntEnum):
    """Standard-io enum object"""

    stdin = 0
    stdout = 1
    stderr = 2


def fspath(fspath: FsPath) -> str:
    """Alias for os._fspath; returns fspath string for any type of path"""
    return _fspath(fspath)


def isfile(fspath: FsPath) -> bool:
    """Return True if the given path is a file; False otherwise"""
    return path.isfile(_fspath(fspath))


def isdir(fspath: FsPath) -> bool:
    """Return True if the given path is a directory; False otherwise"""
    return path.isdir(_fspath(fspath))


def islink(fspath: FsPath) -> bool:
    """Return True if the given path is a link; False otherwise"""
    return path.islink(_fspath(fspath))


def exists(fspath: FsPath) -> bool:
    """Return True if the given path exists; False otherwise"""
    return path.exists(_fspath(fspath))


is_dir = isdir
is_file = isfile
is_link = islink


def safepath(fspath: FsPath) -> str:
    """Check if a file/dir path is save/unused; returns an unused path.

    Args:
        fspath: file-system path; file or directory path string or Path obj

    Returns:
        str: file/dir path that does not exist and contains the given path

    """
    path_str = str(fspath)
    if path.exists(path_str):
        f_bn, f_ext = path.splitext(path_str)
        for n in count(1):
            safe_save_path = f"{f_bn}_{str(n).zfill(3)}.{f_ext}"
            if not path.exists(safe_save_path):
                return safe_save_path
    return path_str


def filesize(fspath: FsPath) -> int:
    """Return the size of the given file(path) in bytes

    Args:
        fspath (FsPath): Filepath as a string or pathlib.Path object

    Returns:
        int: size of the fspath in bytes

    """
    return stat(fspath).st_size


def scandir(dirpath: FsPath = ".") -> Iterable[DirEntry[AnyStr]]:
    """Typed version of os.scandir"""
    if not isdir(dirpath):
        raise NotADirectoryError(f"{dirpath} is not a directory")
    return cast("Iterable[DirEntry[AnyStr]]", _scandir(fspath(dirpath)))


def scandir_list(dirpath: FsPath = ".") -> List[DirEntry[AnyStr]]:
    """Return a list of os.DirEntry objects

    Args:
        dirpath: Dirpath to scan

    Returns:
        List[DirEntry]: List of os.DirEntry objects

    """
    return list(scandir(dirpath))


def scandir_gen_filter(
    it: Union[Iterator[DirEntry[AnyStr]], Iterable[DirEntry[AnyStr]]],
    *,
    follow_symlinks: bool = True,
    files: bool = True,
    dirs: bool = True,
    symlinks: bool = True,
    files_only: bool = False,
    dirs_only: bool = False,
    symlinks_only: bool = False,
) -> Iterator[DirEntry[AnyStr]]:
    if files and dirs and symlinks:  # all
        return (x for x in it)
    elif files_only or (files and not dirs and not symlinks):  # files (only)
        return (el for el in it if el.is_file(follow_symlinks=follow_symlinks))
    elif dirs_only or (not files and dirs and not symlinks):  # dirs only
        return (el for el in it if el.is_dir(follow_symlinks=follow_symlinks))
    elif symlinks_only or (not files and not dirs and symlinks):  # symlinks
        return (el for el in it if el.is_symlink())
    elif files and dirs and not symlinks:  # files and dirs
        return (el for el in it if not el.is_symlink())
    elif files and not dirs and symlinks:  # files and symlinks
        return (el for el in it if not el.is_dir(follow_symlinks=follow_symlinks))
    elif not files and dirs and symlinks:  # dirs and symlinks
        return (el for el in it if not el.is_file(follow_symlinks=follow_symlinks))
    raise ValueError(
        f"Invalid combination of arguments: files={files}, dirs={dirs}, symlinks={symlinks}"
    )


def scandir_gen(
    fspath: FsPath = ".",
    *,
    recursive: bool = False,
    follow_symlinks: bool = True,
    files: bool = True,
    dirs: bool = True,
    symlinks: bool = True,
    files_only: bool = False,
    dirs_only: bool = False,
    symlinks_only: bool = False,
) -> Iterator[DirEntry[str]]:
    r"""Return an iterator of os.DirEntry objects

    Args:
        fspath: (FsPath): dirpath to look through
        files (bool): include files
        dirs (bool): include directories
        symlinks (bool): include symlinks
        follow_symlinks (bool): follow symlinks when checking for dirs and files

    Returns:
        Iterator[DirEntry]: Iterator of os.DirEntry objects

    Raises:
        ValueError: if any of the kwargs (`dirs`, `files` and `symlinks`) are not True

    """
    if not recursive:
        return scandir_gen_filter(
            scandir(fspath),
            follow_symlinks=follow_symlinks,
            files=files,
            dirs=dirs,
            symlinks=symlinks,
            files_only=files_only,
            dirs_only=dirs_only,
            symlinks_only=symlinks_only,
        )

    return scandir_gen_filter(
        chain(
            scandir(fspath),
            *(
                scandir_gen(
                    el.path,
                    recursive=True,
                    follow_symlinks=follow_symlinks,
                    files=files,
                    dirs=True,
                    symlinks=symlinks,
                    files_only=files_only,
                    dirs_only=dirs_only,
                    symlinks_only=symlinks_only,
                )
                for el in scandir(fspath)
                if el.is_dir(follow_symlinks=follow_symlinks)
            ),
        ),
        follow_symlinks=follow_symlinks,
        files=files,
        dirs=dirs,
        symlinks=symlinks,
        files_only=files_only,
        dirs_only=dirs_only,
        symlinks_only=symlinks_only,
    )


def listdir_gen(
    fspath: FsPath = ".",
    *,
    abspath: bool = False,
    follow_symlinks: bool = True,
    files: bool = True,
    dirs: bool = True,
    symlinks: bool = False,
    files_only: bool = False,
    dirs_only: bool = False,
    symlinks_only: bool = False,
) -> Iterator[Path]:
    r"""Return an iterator of strings from DirEntries

    Examples
        >>> tmpdir = 'listdir_gen.doctest'
        >>> from shellfish import sh
        >>> from os import makedirs, path, chdir
        >>> from shutil import rmtree
        >>> _makedirs(tmpdir, exist_ok=True)
        >>> sh.cd(tmpdir)
        >>> filepath_parts = [
        ...     ("dir", "file1.txt"),
        ...     ("dir", "file2.txt"),
        ...     ("dir", "file3.txt"),
        ...     ("dir", "data1.json"),
        ...     ("dir", "dir2", "file1.txt"),
        ...     ("dir", "dir2", "file2.txt"),
        ...     ("dir", "dir2", "file3.txt"),
        ...     ("dir", "dir2a", "file1.txt"),
        ...     ("dir", "dir2a", "file2.txt"),
        ...     ("dir", "dir2a", "file3.txt"),
        ... ]
        >>> from shellfish.fs import touch
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f)
        ...     fspath = path.join(tmpdir, fspath)
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     _makedirs(dirpath, exist_ok=True)
        ...     touch(fspath)
        >>> dirpath = path.join(tmpdir, 'dir')
        >>> dirpath.replace("\\", "/")
        'listdir_gen.doctest/dir'
        >>> sorted(listdir_gen(dirpath, dirs=False, symlinks=False))
        ['data1.json', 'file1.txt', 'file2.txt', 'file3.txt']
        >>> abspaths = sorted(listdir_gen(dirpath, abspath=True, dirs=False, symlinks=False))
        >>> for abspath in [p.replace("\\", "/") for p in abspaths]:
        ...    print(abspath)
        listdir_gen.doctest/dir/data1.json
        listdir_gen.doctest/dir/file1.txt
        listdir_gen.doctest/dir/file2.txt
        listdir_gen.doctest/dir/file3.txt
        >>> rmtree(tmpdir)

    """
    _attr = "path" if abspath else "name"
    return (
        getattr(el, _attr)
        for el in scandir_gen(
            fspath,
            follow_symlinks=follow_symlinks,
            files=files,
            dirs=dirs,
            symlinks=symlinks,
            files_only=files_only,
            dirs_only=dirs_only,
            symlinks_only=symlinks_only,
        )
    )


def filepath_mtimedelta_sec(filepath: FsPath) -> float:
    """Return the seconds since the file(path) was last modified"""
    return time() - path.getmtime(_fspath(filepath))


def touch(fspath: FsPath) -> None:
    """Create an empty file given a fspath

    Args:
        fspath (FsPath): File-system path for where to make an empty file

    """
    if not path.exists(str(fspath)):
        _makedirs(path.dirname(str(fspath)), exist_ok=True)
        with open(fspath, "a"):
            utime(fspath, None)


def files_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = True,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Iterator[str]:
    r"""Yield file-paths beneath a given dirpath (defaults to os.getcwd())

    Args:
        dirpath: Directory path to walk down/through.
        abspath (bool): Yield the absolute path
        onerror: Function called on OSError
        topdown: Not applicable
        followlinks: Follow links
        check: Check that dir exists

    Returns:
        Generator object that yields file-paths (absolute or relative)

    Examples:
        >>> tmpdir = 'files_gen.doctest'
        >>> from os import makedirs; _makedirs(tmpdir, exist_ok=True)
        >>> filepath_parts = [
        ...     ("dir", "file1.txt"),
        ...     ("dir", "file2.txt"),
        ...     ("dir", "file3.txt"),
        ...     ("dir", "dir2", "file1.txt"),
        ...     ("dir", "dir2", "file2.txt"),
        ...     ("dir", "dir2", "file3.txt"),
        ...     ("dir", "dir2a", "file1.txt"),
        ...     ("dir", "dir2a", "file2.txt"),
        ...     ("dir", "dir2a", "file3.txt"),
        ... ]
        >>> from shellfish.fs import touch
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f)
        ...     fspath = path.join(tmpdir, fspath)
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     _makedirs(dirpath, exist_ok=True)
        ...     touch(fspath)
        >>> from pprint import pprint
        >>> expected_files = [el.replace('\\', '/') for el in expected_files]
        >>> pprint(expected_files)
        ['files_gen.doctest/dir/file1.txt',
         'files_gen.doctest/dir/file2.txt',
         'files_gen.doctest/dir/file3.txt',
         'files_gen.doctest/dir/dir2/file1.txt',
         'files_gen.doctest/dir/dir2/file2.txt',
         'files_gen.doctest/dir/dir2/file3.txt',
         'files_gen.doctest/dir/dir2a/file1.txt',
         'files_gen.doctest/dir/dir2a/file2.txt',
         'files_gen.doctest/dir/dir2a/file3.txt']
        >>> files_list = list(sorted(set(files_gen(tmpdir))))
        >>> files_list = [el.replace('\\', '/') for el in files_list]
        >>> pprint(files_list)
        ['files_gen.doctest/dir/dir2/file1.txt',
         'files_gen.doctest/dir/dir2/file2.txt',
         'files_gen.doctest/dir/dir2/file3.txt',
         'files_gen.doctest/dir/dir2a/file1.txt',
         'files_gen.doctest/dir/dir2a/file2.txt',
         'files_gen.doctest/dir/dir2a/file3.txt',
         'files_gen.doctest/dir/file1.txt',
         'files_gen.doctest/dir/file2.txt',
         'files_gen.doctest/dir/file3.txt']
        >>> pprint(list(sorted(set(expected_files))))
        ['files_gen.doctest/dir/dir2/file1.txt',
         'files_gen.doctest/dir/dir2/file2.txt',
         'files_gen.doctest/dir/dir2/file3.txt',
         'files_gen.doctest/dir/dir2a/file1.txt',
         'files_gen.doctest/dir/dir2a/file2.txt',
         'files_gen.doctest/dir/dir2a/file3.txt',
         'files_gen.doctest/dir/file1.txt',
         'files_gen.doctest/dir/file2.txt',
         'files_gen.doctest/dir/file3.txt']
        >>> list(sorted(set(files_list))) == list(sorted(set(expected_files)))
        True
        >>> from shutil import rmtree
        >>> rmtree(tmpdir)

    """
    dirpath = str(dirpath)
    if check and not isdir(dirpath):
        raise NotADirectoryError(dirpath)
    return (
        filepath if abspath else str(filepath).replace(dirpath, "").strip(sep)
        for filepath in (
            path.join(pwd, filename)
            for pwd, dirs, files in walk(
                str(dirpath),
                topdown=topdown,
                onerror=onerror,
                followlinks=followlinks,
            )
            for filename in files
        )
    )


def dirs_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = True,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Iterator[str]:
    r"""Yield directory-paths beneath a dirpath (defaults to os.getcwd())

    Args:
        dirpath: Directory path to walk down/through.
        abspath (bool): Yield the absolute path
        onerror: Function called on OSError
        topdown: Not applicable
        followlinks: Follow links

    Returns:
        Generator object that yields directory paths (absolute or relative)

    Examples:
        >>> tmpdir = 'dirs_gen.doctest'
        >>> from os import makedirs; _makedirs(tmpdir, exist_ok=True)
        >>> filepath_parts = [
        ...     ("dir", "file1.txt"),
        ...     ("dir", "file2.txt"),
        ...     ("dir", "file3.txt"),
        ...     ("dir", "dir2", "file1.txt"),
        ...     ("dir", "dir2", "file2.txt"),
        ...     ("dir", "dir2", "file3.txt"),
        ...     ("dir", "dir2a", "file1.txt"),
        ...     ("dir", "dir2a", "file2.txt"),
        ...     ("dir", "dir2a", "file3.txt"),
        ... ]
        >>> from shellfish.fs import touch
        >>> expected_dirs = []
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f)
        ...     fspath = path.join(tmpdir, fspath)
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     expected_dirs.append(dirpath)
        ...     _makedirs(dirpath, exist_ok=True)
        ...     touch(fspath)
        >>> expected_dirs = list(sorted(set(expected_dirs)))
        >>> from pprint import pprint
        >>> expected_files = [el.replace('\\', '/') for el in expected_files]
        >>> pprint(expected_files)
        ['dirs_gen.doctest/dir/file1.txt',
         'dirs_gen.doctest/dir/file2.txt',
         'dirs_gen.doctest/dir/file3.txt',
         'dirs_gen.doctest/dir/dir2/file1.txt',
         'dirs_gen.doctest/dir/dir2/file2.txt',
         'dirs_gen.doctest/dir/dir2/file3.txt',
         'dirs_gen.doctest/dir/dir2a/file1.txt',
         'dirs_gen.doctest/dir/dir2a/file2.txt',
         'dirs_gen.doctest/dir/dir2a/file3.txt']
        >>> expected_dirs = [el.replace('\\', '/') for el in expected_dirs]
        >>> pprint(expected_dirs)
        ['dirs_gen.doctest/dir',
         'dirs_gen.doctest/dir/dir2',
         'dirs_gen.doctest/dir/dir2a']
        >>> _files = list(files_gen(tmpdir))
        >>> _dirs = list(dirs_gen(tmpdir))
        >>> files_n_dirs_list = list(sorted(set(_files + _dirs)))
        >>> files_n_dirs_list = [el.replace('\\', '/') for el in files_n_dirs_list]
        >>> pprint(files_n_dirs_list)
        ['dirs_gen.doctest',
         'dirs_gen.doctest/dir',
         'dirs_gen.doctest/dir/dir2',
         'dirs_gen.doctest/dir/dir2/file1.txt',
         'dirs_gen.doctest/dir/dir2/file2.txt',
         'dirs_gen.doctest/dir/dir2/file3.txt',
         'dirs_gen.doctest/dir/dir2a',
         'dirs_gen.doctest/dir/dir2a/file1.txt',
         'dirs_gen.doctest/dir/dir2a/file2.txt',
         'dirs_gen.doctest/dir/dir2a/file3.txt',
         'dirs_gen.doctest/dir/file1.txt',
         'dirs_gen.doctest/dir/file2.txt',
         'dirs_gen.doctest/dir/file3.txt']
        >>> expected = sorted(set(expected_files + expected_dirs + [tmpdir]))
        >>> expected = [el.replace('\\', '/') for el in expected]
        >>> pprint(expected)
        ['dirs_gen.doctest',
         'dirs_gen.doctest/dir',
         'dirs_gen.doctest/dir/dir2',
         'dirs_gen.doctest/dir/dir2/file1.txt',
         'dirs_gen.doctest/dir/dir2/file2.txt',
         'dirs_gen.doctest/dir/dir2/file3.txt',
         'dirs_gen.doctest/dir/dir2a',
         'dirs_gen.doctest/dir/dir2a/file1.txt',
         'dirs_gen.doctest/dir/dir2a/file2.txt',
         'dirs_gen.doctest/dir/dir2a/file3.txt',
         'dirs_gen.doctest/dir/file1.txt',
         'dirs_gen.doctest/dir/file2.txt',
         'dirs_gen.doctest/dir/file3.txt']
        >>> files_n_dirs_list == expected
        True
        >>> from shutil import rmtree
        >>> rmtree(tmpdir)

    """
    if check and not isdir(dirpath):
        raise NotADirectoryError(dirpath)
    return (
        dirpath if abspath else str(dirpath).replace(dirpath, "").strip(sep)
        for dirpath in (
            pwd
            for pwd, dirs, files in walk(
                str(dirpath),
                onerror=onerror,
                topdown=topdown,
                followlinks=followlinks,
            )
        )
    )


def files_dirs_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = True,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Tuple[Iterator[str], Iterator[str]]:
    r"""Return a files_gen() and a dirs_gen() in one swell-foop

    Args:
        dirpath: Directory path to walk down/through.
        abspath (bool): Yield the absolute path
        onerror: Function called on OSError
        topdown: Not applicable
        followlinks: Follow links

    Returns:
        A tuple of two generators (files_gen(), dirs_gen())


    Examples:
        >>> tmpdir = 'files_dirs_gen.doctest'
        >>> from os import makedirs; _makedirs(tmpdir, exist_ok=True)
        >>> filepath_parts = [
        ...     ("dir", "file1.txt"),
        ...     ("dir", "file2.txt"),
        ...     ("dir", "file3.txt"),
        ...     ("dir", "dir2", "file1.txt"),
        ...     ("dir", "dir2", "file2.txt"),
        ...     ("dir", "dir2", "file3.txt"),
        ...     ("dir", "dir2a", "file1.txt"),
        ...     ("dir", "dir2a", "file2.txt"),
        ...     ("dir", "dir2a", "file3.txt"),
        ... ]
        >>> from shellfish.fs import touch
        >>> expected_dirs = []
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f)
        ...     fspath = path.join(tmpdir, fspath)
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     expected_dirs.append(dirpath)
        ...     _makedirs(dirpath, exist_ok=True)
        ...     touch(fspath)
        >>> expected_dirs = list(sorted(set(expected_dirs)))
        >>> from pprint import pprint
        >>> expected_files = [el.replace('\\', '/') for el in expected_files]
        >>> pprint(expected_files)
        ['files_dirs_gen.doctest/dir/file1.txt',
         'files_dirs_gen.doctest/dir/file2.txt',
         'files_dirs_gen.doctest/dir/file3.txt',
         'files_dirs_gen.doctest/dir/dir2/file1.txt',
         'files_dirs_gen.doctest/dir/dir2/file2.txt',
         'files_dirs_gen.doctest/dir/dir2/file3.txt',
         'files_dirs_gen.doctest/dir/dir2a/file1.txt',
         'files_dirs_gen.doctest/dir/dir2a/file2.txt',
         'files_dirs_gen.doctest/dir/dir2a/file3.txt']
        >>> expected_dirs = [el.replace('\\', '/') for el in expected_dirs]
        >>> pprint(expected_dirs)
        ['files_dirs_gen.doctest/dir',
         'files_dirs_gen.doctest/dir/dir2',
         'files_dirs_gen.doctest/dir/dir2a']
        >>> _files, _dirs = files_dirs_gen(tmpdir)
        >>> _files = list(_files)
        >>> _dirs = list(_dirs)
        >>> files_n_dirs_list = list(sorted(set(_files + _dirs)))
        >>> files_n_dirs_list = [el.replace('\\', '/') for el in files_n_dirs_list]
        >>> pprint(files_n_dirs_list)
        ['files_dirs_gen.doctest',
         'files_dirs_gen.doctest/dir',
         'files_dirs_gen.doctest/dir/dir2',
         'files_dirs_gen.doctest/dir/dir2/file1.txt',
         'files_dirs_gen.doctest/dir/dir2/file2.txt',
         'files_dirs_gen.doctest/dir/dir2/file3.txt',
         'files_dirs_gen.doctest/dir/dir2a',
         'files_dirs_gen.doctest/dir/dir2a/file1.txt',
         'files_dirs_gen.doctest/dir/dir2a/file2.txt',
         'files_dirs_gen.doctest/dir/dir2a/file3.txt',
         'files_dirs_gen.doctest/dir/file1.txt',
         'files_dirs_gen.doctest/dir/file2.txt',
         'files_dirs_gen.doctest/dir/file3.txt']
        >>> expected = sorted(set(expected_files + expected_dirs + [tmpdir]))
        >>> expected = [el.replace('\\', '/') for el in expected]
        >>> pprint(expected)
        ['files_dirs_gen.doctest',
         'files_dirs_gen.doctest/dir',
         'files_dirs_gen.doctest/dir/dir2',
         'files_dirs_gen.doctest/dir/dir2/file1.txt',
         'files_dirs_gen.doctest/dir/dir2/file2.txt',
         'files_dirs_gen.doctest/dir/dir2/file3.txt',
         'files_dirs_gen.doctest/dir/dir2a',
         'files_dirs_gen.doctest/dir/dir2a/file1.txt',
         'files_dirs_gen.doctest/dir/dir2a/file2.txt',
         'files_dirs_gen.doctest/dir/dir2a/file3.txt',
         'files_dirs_gen.doctest/dir/file1.txt',
         'files_dirs_gen.doctest/dir/file2.txt',
         'files_dirs_gen.doctest/dir/file3.txt']
        >>> files_n_dirs_list == expected
        True
        >>> from shutil import rmtree
        >>> rmtree(tmpdir)

    """
    return files_gen(
        dirpath,
        abspath=abspath,
        followlinks=followlinks,
        onerror=onerror,
        topdown=topdown,
        check=check,
    ), dirs_gen(
        dirpath,
        abspath=abspath,
        followlinks=followlinks,
        onerror=onerror,
        topdown=topdown,
        check=check,
    )


def walk_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = True,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Iterator[str]:
    r"""Yield all paths beneath a given dirpath (defaults to os.getcwd())

    Args:
        dirpath: Directory path to walk down/through.
        abspath (bool): Yield the absolute path
        onerror: Function called on OSError
        topdown: Not applicable
        followlinks: Follow links

    Returns:
        Generator object that yields directory paths (absolute or relative)

    Examples:
        >>> tmpdir = 'walk_gen.doctest'
        >>> from os import makedirs; _makedirs(tmpdir, exist_ok=True)
        >>> filepath_parts = [
        ...     ("dir", "file1.txt"),
        ...     ("dir", "file2.txt"),
        ...     ("dir", "file3.txt"),
        ...     ("dir", "dir2", "file1.txt"),
        ...     ("dir", "dir2", "file2.txt"),
        ...     ("dir", "dir2", "file3.txt"),
        ...     ("dir", "dir2a", "file1.txt"),
        ...     ("dir", "dir2a", "file2.txt"),
        ...     ("dir", "dir2a", "file3.txt"),
        ... ]
        >>> from shellfish.fs import touch
        >>> expected_dirs = []
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f).replace('\\', '/')
        ...     fspath = path.join(tmpdir, fspath).replace('\\', '/')
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     expected_dirs.append(dirpath)
        ...     _makedirs(dirpath, exist_ok=True)
        ...     touch(fspath)
        >>> expected_dirs = [el.replace('\\', '/') for el in sorted(set(expected_dirs))]
        >>> from pprint import pprint
        >>> pprint(expected_files)
        ['walk_gen.doctest/dir/file1.txt',
         'walk_gen.doctest/dir/file2.txt',
         'walk_gen.doctest/dir/file3.txt',
         'walk_gen.doctest/dir/dir2/file1.txt',
         'walk_gen.doctest/dir/dir2/file2.txt',
         'walk_gen.doctest/dir/dir2/file3.txt',
         'walk_gen.doctest/dir/dir2a/file1.txt',
         'walk_gen.doctest/dir/dir2a/file2.txt',
         'walk_gen.doctest/dir/dir2a/file3.txt']
        >>> pprint(expected_dirs)
        ['walk_gen.doctest/dir',
         'walk_gen.doctest/dir/dir2',
         'walk_gen.doctest/dir/dir2a']
        >>> walk_gen_list = list(sorted(set(walk_gen(tmpdir))))
        >>> walk_gen_list = [el.replace('\\', '/') for el in walk_gen_list]
        >>> pprint(walk_gen_list)
        ['walk_gen.doctest',
         'walk_gen.doctest/dir',
         'walk_gen.doctest/dir/dir2',
         'walk_gen.doctest/dir/dir2/file1.txt',
         'walk_gen.doctest/dir/dir2/file2.txt',
         'walk_gen.doctest/dir/dir2/file3.txt',
         'walk_gen.doctest/dir/dir2a',
         'walk_gen.doctest/dir/dir2a/file1.txt',
         'walk_gen.doctest/dir/dir2a/file2.txt',
         'walk_gen.doctest/dir/dir2a/file3.txt',
         'walk_gen.doctest/dir/file1.txt',
         'walk_gen.doctest/dir/file2.txt',
         'walk_gen.doctest/dir/file3.txt']
        >>> expected = sorted(set(expected_files + expected_dirs + [tmpdir]))
        >>> pprint(expected)
        ['walk_gen.doctest',
         'walk_gen.doctest/dir',
         'walk_gen.doctest/dir/dir2',
         'walk_gen.doctest/dir/dir2/file1.txt',
         'walk_gen.doctest/dir/dir2/file2.txt',
         'walk_gen.doctest/dir/dir2/file3.txt',
         'walk_gen.doctest/dir/dir2a',
         'walk_gen.doctest/dir/dir2a/file1.txt',
         'walk_gen.doctest/dir/dir2a/file2.txt',
         'walk_gen.doctest/dir/dir2a/file3.txt',
         'walk_gen.doctest/dir/file1.txt',
         'walk_gen.doctest/dir/file2.txt',
         'walk_gen.doctest/dir/file3.txt']
        >>> walk_gen_list == expected
        True
        >>> from shutil import rmtree
        >>> rmtree(tmpdir)

    """
    dirpath = str(dirpath)
    if check and not isdir(dirpath):
        raise NotADirectoryError(dirpath)
    return (
        str(path_string)
        if abspath
        else str(path_string).replace(dirpath, "").strip(sep)
        for path_string in chain.from_iterable(
            (
                pwd,
                *(path.join(pwd, _dir) for _dir in dirs),
                *(path.join(pwd, _file) for _file in files),
            )
            for pwd, dirs, files in walk(
                dirpath,
                topdown=topdown,
                followlinks=followlinks,
                onerror=onerror,
            )
        )
    )


def filepath_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = False,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Iterator[Path]:
    r"""Yield all filepaths as pathlib.Path objects beneath a dirpath"""
    return (
        Path(el)
        for el in files_gen(
            dirpath=dirpath,
            abspath=abspath,
            topdown=topdown,
            onerror=onerror,
            followlinks=followlinks,
            check=check,
        )
    )


def dirpath_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = False,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Iterator[Path]:
    r"""Yield all dirpaths as pathlib.Path objects beneath a dirpath"""
    return (
        Path(el)
        for el in dirs_gen(
            dirpath=dirpath,
            abspath=abspath,
            topdown=topdown,
            onerror=onerror,
            followlinks=followlinks,
            check=check,
        )
    )


def path_gen(
    dirpath: FsPath = ".",
    *,
    abspath: bool = False,
    topdown: bool = True,
    onerror: Optional[Callable[[OSError], Any]] = None,
    followlinks: bool = False,
    check: bool = True,
) -> Iterator[Path]:
    r"""Yield all filepaths as pathlib.Path objects beneath a dirpath"""
    return (
        Path(el)
        for el in walk_gen(
            dirpath=dirpath,
            abspath=abspath,
            topdown=topdown,
            onerror=onerror,
            followlinks=followlinks,
            check=check,
        )
    )


def wbytes(
    filepath: FsPath,
    bites: bytes,
    *,
    append: bool = False,
    chmod: Optional[int] = None,
) -> int:
    """Write/Save bytes to a fspath

    The parameter 'bites' is used instead of 'bytes' to not redefine the
    built-in python bytes object.

    Args:
        filepath: fspath to write to
        bites: Bytes to be written
        append (bool): Append to the file if True, overwrite otherwise; default
            is False
        chmod (Optional[int]): chmod the file after writing; default is None

    Returns:
        int: Number of bytes written

    Examples:
        >>> from shellfish.fs import rbytes, wbytes
        >>> fspath = "wbytes.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> wbytes(fspath, bites_to_save)
        20
        >>> rbytes(fspath)
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    _write_mode = "ab" if append else "wb"
    with open(filepath, _write_mode) as fd:
        nbytes = fd.write(bites)
    if chmod is not None:
        _chmod(filepath, chmod)
    return nbytes


def rbytes(filepath: FsPath) -> bytes:
    """Load/Read bytes from a fspath

    Args:
        filepath: fspath read as bytes

    Returns:
        bytes from the fspath

    Examples:
        >>> from shellfish.fs import rbytes, wbytes
        >>> fspath = "rbytes.doctest.txt"
        >>> bites_to_save = b"These are some bytes"
        >>> wbytes(fspath, bites_to_save)
        20
        >>> bites_to_save  # they are bytes!
        b'These are some bytes'
        >>> rbytes(fspath)
        b'These are some bytes'
        >>> import os; os.remove(fspath)

    """
    with open(filepath, "rb") as file:
        return bytes(file.read())


def file_lines_gen(filepath: FsPath, keepends: bool = True) -> Iterable[str]:
    r"""Yield lines from a given fspath

    Args:
        filepath: File to yield lines from
        keepends: Flag to keep the ends of the file lines

    Yields:
        Lines from the given fspath

    Examples:
        >>> string = '\n'.join(str(i) for i in range(1, 10))
        >>> string
        '1\n2\n3\n4\n5\n6\n7\n8\n9'
        >>> fspath = "file_lines_gen.doctest.txt"
        >>> from shellfish.fs import wstring
        >>> wstring(fspath, string)
        17
        >>> for file_line in file_lines_gen(fspath):
        ...     file_line
        '1\n'
        '2\n'
        '3\n'
        '4\n'
        '5\n'
        '6\n'
        '7\n'
        '8\n'
        '9'
        >>> for file_line in file_lines_gen(fspath, keepends=False):
        ...     file_line
        '1'
        '2'
        '3'
        '4'
        '5'
        '6'
        '7'
        '8'
        '9'
        >>> import os; os.remove(fspath)


    """
    with open(filepath) as f:
        if keepends:
            yield from (line for line in f)
        else:
            yield from (line.rstrip("\n").rstrip("\r\n") for line in f)


def rbytes_gen(filepath: FsPath, blocksize: int = 65536) -> Iterable[bytes]:
    """Yield bytes from a given fspath"""
    with open(filepath, "rb") as f:
        while True:
            data = f.read(blocksize)
            if not data:
                break
            yield data


def wbytes_gen(
    filepath: FsPath,
    bytes_gen: Iterable[bytes],
    append: bool = False,
    chmod: Optional[int] = None,
) -> int:
    """Write/Save bytes to a fspath

    Args:
        filepath: fspath to write to
        bytes_gen: Bytes to be written
        append (bool): Append to the file if True, overwrite otherwise; default
            is False
        chmod (Optional[int]): chmod the file after writing; default is None

    Returns:
        int: Number of bytes written

    Examples:
        >>> from shellfish.fs import rbytes, wbytes
        >>> fspath = "wbytes_gen.doctest.txt"
        >>> bites_to_save = (b"These are some bytes... ", b"more bytes!")
        >>> bites_to_save  # they are bytes!
        (b'These are some bytes... ', b'more bytes!')
        >>> wbytes_gen(fspath, (b for b in bites_to_save))
        35
        >>> rbytes(fspath)
        b'These are some bytes... more bytes!'
        >>> import os; os.remove(fspath)

    """
    _mode: Literal["ab", "wb"] = const.ab if append else const.wb
    with open(filepath, mode=_mode) as fd:
        nbytes_written = sum(fd.write(chunk) for chunk in bytes_gen)
    if chmod is not None:
        _chmod(filepath, chmod)
    return nbytes_written


def rstring(filepath: FsPath, *, encoding: str = "utf-8") -> str:
    r"""Load/Read a string given a fspath

    Args:
        filepath: Filepath for file to read
        encoding: Encoding to use for reading the file

    Returns:
        str: String read from given fspath

    Examples:
        ``` python
        >>> from shellfish.fs import rstring, wstring
        >>> fspath = "lstring.doctest.txt"
        >>> sstring(fspath, r'Check out this string')
        21
        >>> lstring(fspath)
        'Check out this string'
        >>> import os; os.remove(fspath)

        ```

    """
    _bytes = rbytes(filepath=filepath)
    try:
        return _bytes.decode(encoding=encoding)
    except UnicodeDecodeError:  # Catch the unicode decode error
        pass
    return _bytes.decode(encoding="latin2")


def wstring(
    filepath: FsPath,
    string: str,
    *,
    encoding: str = "utf-8",
    append: bool = False,
    chmod: Optional[int] = None,
) -> int:
    """Save/Write a string to fspath

    Args:
        filepath: fspath to write to
        string (str): string to be written
        encoding: String encoding to write file with
        append (bool): Flag to append to file; default = False
        chmod (Optional[int]): Optional chmod to set on file

    Returns:
        None

    Examples:
        >>> from shellfish.fs import rstring, wstring
        >>> fspath = "sstring.doctest.txt"
        >>> wstring(fspath, r'Check out this string')
        21
        >>> rstring(fspath)
        'Check out this string'
        >>> import os; os.remove(fspath)

    """
    return wbytes(
        filepath=filepath,
        bites=string.encode(encoding),
        append=append,
        chmod=chmod,
    )


def wjson(
    filepath: FsPath,
    data: Any,
    *,
    fmt: bool = False,
    pretty: bool = False,
    sort_keys: bool = False,
    append_newline: bool = False,
    default: Optional[Callable[[Any], Any]] = None,
    chmod: Optional[int] = None,
    append: bool = False,
    **kwargs: Any,
) -> int:
    """Save/Write json-serial-ize-able data to a fspath

    Args:
        filepath: fspath to write to
        data (Any): json-serial-ize-able data
        fmt (bool): Indented (2 spaces) or minify data (default=False)
        pretty (bool): Indented (2 spaces) or minify data (default=False)
        sort_keys (bool): Sort the data keys if the data is a dictionary.
        append_newline (bool): Sort the data keys if the data is a dictionary.
        default: default function hook
        **kwargs: Additional keyword arguments to pass to jsonbourne.JSON.dumpb

    Returns:
        int: Number of bytes written

    Examples:
        Imports:

        >>> from shellfish.fs import rjson, wjson

        Dictionaries:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> fspath = "rjson_dict.doctest.json"
        >>> wjson(fspath, data)
        19
        >>> rjson(fspath)
        {'a': 1, 'b': 2, 'c': 3}
        >>> import os; os.remove(fspath)

        Lists:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> data = list(data.items())
        >>> data  # has tuples, but will be saved as strings
        [('a', 1), ('b', 2), ('c', 3)]
        >>> fspath = "rjson_dict.doctest.json"
        >>> wjson(fspath, data)
        25
        >>> rjson(fspath)
        [['a', 1], ['b', 2], ['c', 3]]
        >>> os.remove(fspath)


    """
    return wbytes(
        filepath=filepath,
        bites=JSON.dumpb(
            data=data,
            fmt=fmt,
            pretty=pretty,
            append_newline=append_newline,
            default=default,
            sort_keys=sort_keys,
            **kwargs,
        ),
        chmod=chmod,
        append=append,
    )


def rjson(filepath: FsPath) -> Any:
    """Load/Read-&-parse json data given a fspath

    Args:
        filepath: Filepath to load/read data from

    Returns:
        Parsed JSON data

    Examples:
        Imports:

        >>> from shellfish.fs import rjson, wjson

        Dictionaries:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> fspath = "rjson_dict.doctest.json"
        >>> wjson(fspath, data)
        19
        >>> rjson(fspath)
        {'a': 1, 'b': 2, 'c': 3}
        >>> import os; os.remove(fspath)

        Lists:

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> data = list(data.items())
        >>> data  # has tuples, but will be saved as strings
        [('a', 1), ('b', 2), ('c', 3)]
        >>> fspath = "rjson_dict.doctest.json"
        >>> wjson(fspath, data)
        25
        >>> rjson(fspath)
        [['a', 1], ['b', 2], ['c', 3]]
        >>> os.remove(fspath)

    """
    return JSON.loads(lstring(filepath=filepath))


def extension(fspath: str) -> str:
    """Return the extension for a fspath"""
    return "".join(Path(fspath).suffixes).lstrip(".")


def sep_split(fspath: FsPath) -> Tuple[str, ...]:
    """Split a string on the current platform os.path.sep value"""
    return tuple((el for el in str(fspath).split(sep) if el != sep and el != ""))


def sep_join(path_strings: Iterator[str]) -> str:
    """Join iterable of strings on the current platform os.path.sep value"""
    return sep.join(path_strings)


def sep_strip(fspath: FsPath) -> str:
    """Strip a string of the current platform's os.path.sep value"""
    return str(fspath).strip(sep)


def sep_lstrip(fspath: FsPath) -> str:
    """Left-strip a string of the current platform's os.path.sep value"""
    return str(fspath).lstrip(sep)


def sep_rstrip(fspath: FsPath) -> str:
    """Right-strip a string of the current platform's os.path.sep value"""
    return str(fspath).rstrip(sep)


def filecmp(
    left: FsPath,
    right: FsPath,
    *,
    shallow: bool = True,
    blocksize: int = 65536,
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


def shebang(fspath: FsPath) -> Union[None, str]:
    r"""Get the shebang string given a fspath; Returns None if no shebang

    Args:
        fspath (FsPath): Path to file that might have a shebang

    Returns:
        Optional[str]: The shebang string if it exists, None otherwise

    Examples:
        >>> from inspect import getabsfile
        >>> script = 'ashellscript.sh'
        >>> with open(script, 'w') as f:
        ...     f.write('#!/bin/bash\necho "howdy"\n')
        25
        >>> shebang(script)
        '#!/bin/bash'
        >>> from os import remove
        >>> remove(script)

    """
    with open(fspath, "r") as f:
        first = f.readline().replace("\r\n", "\n").strip("\n")
        return first if "#!" in first[:2] else None


def chmod(fspath: FsPath, mode: int) -> None:
    """Change the access permissions of a file

    Args:
        fspath (FsPath): Path to file to chmod
        mode (int): Permissions mode as an int

    """
    return _chmod(path=str(fspath), mode=mode)


def mkdir(
    fspath: FsPath, *, parents: bool = False, p: bool = False, exist_ok: bool = False
) -> None:
    """Make directory at given fspath

    Args:
        fspath (FsPath): Directory path to create
        parents (bool): Make parent dirs if True; do not make parent dirs if False
        p (bool): Make parent dirs if True; do not make parent dirs if False (alias of parents)
        exist_ok (bool): Throw error if directory exists and exist_ok is False

    Returns:
         None

    """
    _parents = parents or p
    if _parents or exist_ok:
        return _makedirs(_fspath(fspath), exist_ok=_parents or exist_ok)
    return _mkdir(_fspath(fspath))


def mkdirp(fspath: FsPath) -> None:
    """Make directory and parents"""
    return mkdir(fspath=fspath, parents=True)


def glob(pattern: str, *, recursive: bool = False, r: bool = False) -> Iterator[str]:
    """Return an iterator of fspaths matching the given glob pattern

    Args:
        fspath: Glob pattern
        recursive: Recursively search directories if True
        r: Recursively search directories if True (Alias for recursive)

    Returns:
        Iterator[str]: Iterator of fspaths matching the glob pattern

    """
    return iglob(pattern, recursive=recursive or r)


def rename(src: FsPath, dest: FsPath, *, dryrun: bool = False) -> Tuple[FsPath, FsPath]:
    if not dryrun:
        _move(src, dest)
    return (src, dest)


def move(src: FsPath, dest: FsPath) -> None:
    """Move file(s) like on the command line

    Args:
        src (FsPath): source file(s)
        dest (FsPath): destination path

    """
    _dst_str = str(dest)
    for file in iglob(str(src), recursive=True):
        _move(file, _dst_str)


def rmfile(fspath: FsPath, *, dryrun: bool = False) -> str:
    """Remove a file at given fspath

    Args:
        fspath (FsPath): Filepath to remove
        dryrun (bool): Do not remove file if True

    Returns:
        None

    """
    if not dryrun:
        remove(_fspath(fspath))
    return _fspath(fspath)


def rmdir(fspath: FsPath, *, recursive: bool = False) -> None:
    """Remove directory at given fspath

    Args:
        fspath (FsPath): Directory path to remove
        recursive (bool): Recursively remove all contents if True

    Returns:
        None

    """
    if recursive:
        return rmtree(_fspath(fspath))
    return _rmdir(_fspath(fspath))


def rm_gen(
    fspath: FsPath,
    *,
    recursive: bool = False,
    dryrun: bool = False,
) -> Generator[str, Any, Any]:
    """Remove files & directories in the style of the shell
    Args:
        fspath (FsPath): Path to file or directory to remove
        recursive (bool): Flag to remove recursively (like the `-r` in `rm -r dir`)
        dryrun (bool): Do not remove file if True

    Raises:
        ValueError: If recursive and r are `False` and fspath is a directory

    """
    if has_magic(str(fspath)):
        if dryrun:
            yield from iglob(_fspath(fspath), recursive=recursive)
        else:
            for _path_str in iglob(str(fspath), recursive=recursive):
                if isfile(_path_str):
                    remove(_path_str)
                elif recursive:
                    rmtree(_path_str)
                else:
                    raise ValueError(
                        f"{str(_path_str)} (under {str(fspath)}) is a directory -- use r=True or recursive=True"
                    )
    else:
        if isfile(fspath):
            if not dryrun:
                remove(_fspath(fspath))
            yield _fspath(fspath)
        elif recursive:
            if not dryrun:
                rmtree(_fspath(fspath))
            yield _fspath(fspath)
        else:
            raise ValueError(
                f"{str(fspath)} is a directory -- use r=True or recursive=True"
            )


def rm(
    fspath: FsPath,
    *,
    recursive: bool = False,
    dryrun: bool = False,
    verbose: bool = False,
) -> Union[List[str], None]:
    """Remove files & directories in the style of the shell
    Args:
        fspath (FsPath): Path to file or directory to remove
        recursive (bool): Flag to remove recursively (like the `-r` in `rm -r dir`)
        dryrun (bool): Do not remove file if True

    Raises:
        ValueError: If recursive and r are `False` and fspath is a directory

    """
    if verbose:
        return list(rm_gen(fspath=fspath, recursive=recursive, dryrun=dryrun))
    else:
        exhaust(rm_gen(fspath=fspath, recursive=recursive, dryrun=dryrun))
        return None


def stat(fspath: FsPath) -> os_stat_result:
    """Return the os.stat_result object for a given fspath

    Args:
        fspath (FsPath): Path to file or directory

    Returns:
        os.stat_result: stat_result object

    """
    return _stat(_fspath(fspath))


SymlinkType = Union[Literal["dir"], Literal["file"], Literal["junction"], str]


def symlink(link: FsPath, target: FsPath, *, _type: SymlinkType = "file") -> None:
    if is_win():
        raise NotImplementedError("TODO")
    _symlink(str(link), str(target))


def copy_file(
    src: FsPath, dest: FsPath, *, dryrun: bool = False, mkdirp: bool = False
) -> None:
    """Copy a file given a source-path and a destination-path

    Args:
        src (str): Source fspath
        dest (str): Destination fspath

    """
    _dest = Path(dest)
    if mkdirp:
        _dest.parent.mkdir(parents=mkdirp, exist_ok=True)
    elif not _dest.parent.exists() or not _dest.parent.is_dir():
        raise FileNotFoundError(f"Destination directory {_dest.parent} does not exist")
    wbytes_gen(dest, lbytes_gen(src, blocksize=2**18))


def cp(
    src: FsPath,
    dest: FsPath,
    *,
    force: bool = True,
    recursive: bool = False,
    r: bool = False,
    f: bool = True,
) -> None:
    """Copy the directory/file src to the directory/file dest

    Args:
        src (str): Source directory/file to copy
        dest: Destination directory/file to copy
        force: Force the copy (like -f flag for cp in shell)
        recursive: Recursive copy (like -r flag for cp in shell)
        r: alias for recursive
        f: alias for force

    Raises:
        ValueError: If src is a directory and recursive and r are both `False`

    """
    _recursive = recursive or r
    _force = force or f
    for _src in iglob(_fspath(src), recursive=True):
        _dest = dest
        if (path.exists(dest) and not _force) or _src == dest:
            return
        if path.isdir(_src) and not _recursive:
            raise ValueError("Source ({}) is directory; use r=True")
        if path.isfile(_src) and path.isdir(dest):
            _dest = path.join(dest, path.basename(_src))
        if path.isfile(_src) or path.islink(src):
            copy_file(_src, _dest)
        if path.isdir(_src):
            if not path.exists(dest):
                _makedirs(dest)
            copytree(src, dest, dirs_exist_ok=True)


# aliases
mv = move

# IO function aliases ~ for backwards compatibility and convenience
lbytes = rbin = lbin = rbytes
sbytes = wbin = sbin = wbytes
lbytes_gen = rbin_gen = rbytes_gen
sbytes_gen = wbin_gen = wbytes_gen
lstring = rstr = lstr = rstring
sstring = wstr = sstr = wstring
ljson = rjson
sjson = wjson

# module exports
__all__ = (
    "Stdio",
    "SymlinkType",
    "__version__",
    "chmod",
    "copy_file",
    "cp",
    "dirpath_gen",
    "dirs_gen",
    "exists",
    "exists_async",
    "extension",
    "file_lines_gen",
    "filecmp",
    "filepath_gen",
    "filepath_mtimedelta_sec",
    "files_dirs_gen",
    "files_gen",
    "filesize",
    "filesize_async",
    "fspath",
    "is_dir",
    "is_dir_async",
    "is_file",
    "is_file_async",
    "is_link",
    "is_link_async",
    "isdir",
    "isdir_async",
    "isfile",
    "isfile_async",
    "islink",
    "islink_async",
    "lbin",
    "lbytes",
    "lbytes_async",
    "lbytes_gen",
    "lbytes_gen_async",
    "listdir_gen",
    "ljson",
    "ljson_async",
    "lstat_async",
    "lstr",
    "lstr_async",
    "lstring",
    "lstring_async",
    "mkdir",
    "mkdirp",
    "move",
    "mv",
    "path_gen",
    "rbin",
    "rbin_async",
    "rbin_gen",
    "rbin_gen_async",
    "rbytes",
    "rbytes_async",
    "rbytes_gen",
    "rbytes_gen_async",
    "rename",
    "rjson",
    "rjson_async",
    "rm",
    "rm_gen",
    "rmdir",
    "rmfile",
    "rstr",
    "rstr_async",
    "rstring",
    "rstring_async",
    "safepath",
    "sbin",
    "sbin_async",
    "sbytes",
    "sbytes_async",
    "sbytes_gen",
    "sbytes_gen_async",
    "scandir",
    "scandir_gen",
    "scandir_list",
    "sep_join",
    "sep_lstrip",
    "sep_rstrip",
    "sep_split",
    "sep_strip",
    "shebang",
    "sjson",
    "sjson_async",
    "sstr",
    "sstr_async",
    "sstring",
    "sstring_async",
    "stat",
    "stat_async",
    "symlink",
    "touch",
    "walk_gen",
    "wbin",
    "wbin_async",
    "wbin_gen",
    "wbin_gen_async",
    "wbytes",
    "wbytes_async",
    "wbytes_gen",
    "wbytes_gen_async",
    "wjson",
    "wjson_async",
    "wstr",
    "wstr_async",
    "wstring",
    "wstring_async",
)
