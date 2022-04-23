# -*- coding: utf-8 -*-
"""Directory tree"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterator, Optional, Union


class _DirTree:
    """DirTree object for use by the tree command"""

    _filename_prefix_mid: str = "├──"
    _filename_prefix_last: str = "└──"
    _parent_prefix_middle: str = "    "
    _parent_refix_last: str = "│   "

    path: Path
    is_last: bool
    depth: int
    parent: Optional[_DirTree]

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
        while parent and parent.parent is not None:  # type: ignore[truthy-bool]
            parts.append(
                self._parent_prefix_middle
                if parent.is_last
                else self._parent_refix_last
            )
            parent = parent.parent

        return "".join(reversed(parts))
