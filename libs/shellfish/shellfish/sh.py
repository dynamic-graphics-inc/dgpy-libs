# -*- coding: utf-8 -*-
"""shell utils"""
from distutils.dir_util import copy_tree
from enum import IntEnum
from functools import lru_cache
from glob import iglob
from os import (
    chdir,
    chmod as _chmod,
    environ,
    fspath as _fspath,
    getcwd,
    listdir,
    makedirs,
    mkdir as _mkdir,
    path,
    remove,
    scandir,
)
from pathlib import Path
from shlex import split as _shplit
from shutil import move, rmtree, which as _which

from shellfish import fs
from xtyping import IO, Any, Callable, FsPath, Iterator, List, Optional, Tuple, Union

__all__og = (
    "Flag",
    "Stdio",
    "cd",
    "echo",
    "export",
    "setenv",
    "which",
    "touch",
    "which_lru",
    "where",
)

__all__ = (
    "Stdio",
    "shplit",
    "basename",
    "cd",
    "chmod",
    "cp",
    "cp_dir",
    "cp_file",
    "dirname",
    "echo",
    "export",
    "ls",
    "ls_dirs",
    "ls_files",
    "ls_files_dirs",
    "mkdir",
    "mkdirp",
    "mv",
    "pwd",
    "rm",
    "setenv",
    "touch",
    "tree",
    "where",
    "which",
    "which_lru",
    "source",
)


class Stdio(IntEnum):
    """Standard-io enum object"""

    stdin = 0
    stdout = 1
    stderr = 2


class _FlagMeta(type):
    """Meta class"""

    @staticmethod
    @lru_cache(maxsize=None)
    def attr2flag(string: str) -> str:
        """Convert and return attr to string"""
        return string.replace("_", "-")

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

    Examples:
        >>> import os
        >>> pwd() == os.getcwd()
        True

    """
    return getcwd()


def dirname(fspath: FsPath) -> str:
    """Return dirname/parent-dir of given path; alias of os.path.dirname

    Args:
        fspath: File-system path

    Returns:
        str: basename of path

    """
    return path.dirname(_fspath(fspath))


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
    *args: Any, sep: str = " ", end: str = "\n", file: Optional[IO[Any]] = None
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
        f"Unable to parse env variable - key: {str(key)}, value: {str(val)}"
    )


def mkdir(fspath: FsPath, *, p: bool = False, exist_ok: bool = False) -> None:
    """Make directory at given fspath

    Args:
        fspath (FsPath): Directory path to create
        p (bool): Make parent dirs if True; do not make parent dirs if False
        exist_ok (bool): Throw error if directory exists and exist_ok is False

    """
    if p or exist_ok:
        return makedirs(_fspath(fspath), exist_ok=p or exist_ok)
    return _mkdir(_fspath(fspath))


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
    """Alias for shellfish.fs.touch

    Args:
        fspath (FsPath): File-system path for where to make an empty file

    """
    return fs.touch(fspath=fspath)


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


@lru_cache(maxsize=128)
def which_lru(cmd: str, path: Optional[str] = None) -> Optional[str]:
    """Return the result of `shutil.which` and cache the results

    Args:
        cmd (str): Command/exe to find path of
        path (str): System path to use

    Returns:
        Optional[str]: path to command/exe

    """
    return which(cmd, path=path)


class _DirTree:
    """DirTree object for use by the tree command"""

    _filename_prefix_mid: str = "├──"
    _filename_prefix_last: str = "└──"
    _parent_prefix_middle: str = "    "
    _parent_refix_last: str = "│   "

    def __init__(
        self,
        path: Union[str, Path],
        parent_path: Optional["_DirTree"],
        is_last: bool,
    ) -> None:
        """Construct a DirTree object

        Args:
            path: Path-string to start the directory tree at
            parent_path: The parent path to start the directory tree at
            is_last: Is the current tree the last diretory in the tree

        """
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        self.depth: int = self.parent.depth + 1 if self.parent else 0

    @classmethod
    def make_tree(
        cls,
        root: Path,
        parent: Optional["_DirTree"] = None,
        is_last: bool = False,
        filterfn: Optional[Callable[..., bool]] = None,
    ) -> Iterator["_DirTree"]:
        """Make a DirTree object

        Args:
            root: Root directory
            parent: Parent directory
            is_last: Is last
            filterfn: Function to filter with

        Yields:
            DirTree object

        """
        root = Path(str(root))
        filterfn = filterfn or _DirTree._default_filter

        displayable_root = cls(str(root), parent, is_last)
        yield displayable_root

        children = sorted(
            (fspath for fspath in root.iterdir() if filterfn(str(fspath))),
            key=lambda s: str(s).lower(),
        )
        count = 1
        for _path in children:
            is_last = count == len(children)
            if _path.is_dir():
                yield from cls.make_tree(
                    _path,
                    parent=displayable_root,
                    is_last=is_last,
                    filterfn=filterfn,
                )
            else:
                yield cls(_path, displayable_root, is_last)
            count += 1

    @staticmethod
    def _default_filter(path_string: str) -> bool:
        """Return True/False if the fspath is to be filtered/ignored"""
        ignore_strings = (".pyc", "__pycache__")
        return not any(
            ignored in str(path_string).lower() for ignored in ignore_strings
        )

    @property
    def displayname(self) -> str:
        """Diplay name for DirTree root path name

        Returns:
            str: root path name as a string

        """
        if self.path.is_dir():
            return self.path.name + "/"
        return self.path.name

    def displayable(self) -> str:
        """Return displayable tree string

        Returns:
            str: displayable tree string

        """
        if self.parent is None:
            return self.displayname

        _filename_prefix = (
            self._filename_prefix_last if self.is_last else self._filename_prefix_mid
        )

        parts = [f"{_filename_prefix!s} {self.displayname!s}"]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(
                self._parent_prefix_middle
                if parent.is_last
                else self._parent_refix_last
            )
            parent = parent.parent

        return "".join(reversed(parts))


def tree(dirpath: FsPath, filterfn: Optional[Callable[[str], bool]] = None) -> str:
    """Create a directory tree string given a directory path

    Args:
        dirpath (FsPath): Directory string to make tree for
        filterfn: Function to filter sub-directories and sub-files with

    Returns:
        str: Directory-tree string

    Examples:
        >>> tmpdir = 'tree.doctest'
        >>> from os import makedirs; makedirs(tmpdir, exist_ok=True)
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
        >>> from shellfish.sh import touch
        >>> expected_files = []
        >>> for f in filepath_parts:
        ...     fspath = path.join(*f)
        ...     fspath = path.join(tmpdir, fspath)
        ...     dirpath = path.dirname(fspath)
        ...     expected_files.append(fspath)
        ...     makedirs(dirpath, exist_ok=True)
        ...     touch(fspath)
        >>> print(tree(tmpdir))
        tree.doctest/
        └── dir/
            ├── dir2/
            │   ├── file1.txt
            │   ├── file2.txt
            │   └── file3.txt
            ├── dir2a/
            │   ├── file1.txt
            │   ├── file2.txt
            │   └── file3.txt
            ├── file1.txt
            ├── file2.txt
            └── file3.txt
        >>> print(tree(tmpdir, lambda s: _DirTree._default_filter(s) and not "file2" in s))
        tree.doctest/
        └── dir/
            ├── dir2/
            │   ├── file1.txt
            │   └── file3.txt
            ├── dir2a/
            │   ├── file1.txt
            │   └── file3.txt
            ├── file1.txt
            └── file3.txt
        >>> from shutil import rmtree
        >>> rmtree(tmpdir)

    """
    return "\n".join(
        p.displayable() for p in _DirTree.make_tree(Path(dirpath), filterfn=filterfn)
    )


########
## CP ##
########


def cp_file(src: str, target: str) -> None:
    """Copy a file given a source-path and a destination-path

    Args:
        src (str): Source fspath
        target (str): Destination fspath

    """
    try:
        makedirs(path.dirname(target), exist_ok=True)
    except FileNotFoundError:
        pass
    fs.sbytes_gen(target, fs.lbytes_gen(src, blocksize=2 ** 18))


def cp_dir(src: str, target: str) -> None:
    """Copy a directory given a source and destination directory paths

    Args:
        src (str): Source directory path
        target (str): Destination directory path

    """
    if not path.exists(target):
        makedirs(target)
    copy_tree(src, target)


def cp(src: str, target: str, *, force: bool = True, recursive: bool = False) -> None:
    """Copy the directory/file src to the directory/file target

    Args:
        src (str): Source directory/file to copy
        target: Destination directory/file to copy
        force: Force the copy (like -f flag for cp in shell)
        recursive: Recursive copy (like -r flag for cp in shell)

    """
    for src in iglob(src, recursive=True):
        _dest = target
        if (path.exists(target) and not force) or src == target:
            return
        if path.isdir(src) and not recursive:
            raise ValueError("Source ({}) is directory; use r=True")
        if path.isfile(src) and path.isdir(target):
            _dest = path.join(target, path.basename(src))
        if path.isfile(src) or path.islink(src):
            cp_file(src, _dest)
        if path.isdir(src):
            cp_dir(src, _dest)


def rm(fspath: FsPath, *, r: bool = False, v: bool = False) -> None:
    """Remove files & directories in the style of the shell

    Args:
        fspath (FsPath): Path to file or directory to remove
        r (bool): Flag to remove recursively (like the `-r` in `rm -r dir`)
        v (bool): Flag to be verbose

    """
    for _path_str in iglob(str(fspath), recursive=True):
        try:
            remove(_path_str)
            if v:
                echo(f"Removed file: {_path_str}")

        except Exception:
            if r:
                rmtree(_path_str)
                if v:
                    echo(f"Removed dir: {_path_str}")
            else:
                raise ValueError(_path_str + " is a directory -- use r=True")


def ls(dirpath: FsPath = ".", abspath: bool = False) -> List[str]:
    """List files and dirs given a dirpath (defaults to pwd)

    Args:
        dirpath (FsPath): path-string to directory to list
        abspath (bool): Give absolute paths

    Returns:
        List of the directory items

    """
    if abspath:
        return [el.path for el in scandir(str(dirpath))]
    return listdir(str(dirpath))


def ls_files(dirpath: FsPath = ".", *, abspath: bool = False) -> List[str]:
    """List the files in a given directory path

    Args:
        dirpath (FsPath): Directory path for which one might want to list files
        abspath (bool): Return absolute filepaths

    Returns:
        List of files as strings

    """
    files = (el for el in scandir(str(dirpath)) if el.is_file())
    if abspath:
        return list(map(lambda el: el.path, files))
    return list(map(lambda el: el.name, files))


def ls_dirs(dirpath: FsPath = ".", *, abspath: bool = False) -> List[str]:
    """List the directories in a given directory path

    Args:
        dirpath (FsPath): Directory path for which one might want list directories
        abspath (bool): Return absolute directory paths

    Returns:
        List of directories as strings

    """
    dirs = (el for el in scandir(str(dirpath)) if el.is_dir())
    if abspath:
        return list(map(lambda el: el.path, dirs))
    return list(map(lambda el: el.name, dirs))


def ls_files_dirs(
    dirpath: FsPath = ".", *, abspath: bool = False
) -> Tuple[List[str], List[str]]:
    """List the files and directories given directory path

    Args:
        dirpath (FsPath): Directory path to execute on
        abspath (bool): Return absolute file/directory paths

    Returns:
        Two lists of strings; the first is a list of the files and the second
            is a list of the directories

    """
    dir_items = fs.scandir_list(dirpath)
    dir_dir_entries = (el for el in dir_items if el.is_dir())
    file_dir_entries = (el for el in dir_items if el.is_file())
    if not abspath:
        return [el.name for el in file_dir_entries], [el.name for el in dir_dir_entries]
    return [el.path for el in file_dir_entries], [el.path for el in dir_dir_entries]


def mv(src: FsPath, dst: FsPath) -> None:
    """Move file(s) like on the command line

    Args:
        src (FsPath): source file(s)
        dst (FsPath): destination

    """
    _dst_str = str(dst)
    for file in iglob(str(src), recursive=True):
        move(file, _dst_str)


def source(filepath: FsPath, _globals: bool = True) -> None:
    """Execute/run a python file given a fspath and put globals in globasl

    Args:
        filepath (FsPath): Path to python file
        _globals (bool): Exec using globals

    """
    string = fs.lstring(str(filepath))
    if _globals:
        exec(string, globals())
    else:
        exec(string)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
