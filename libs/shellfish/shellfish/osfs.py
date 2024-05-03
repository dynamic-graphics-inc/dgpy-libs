# -*- coding: utf-8 -*-
"""Os specific filesystem utils/operations"""

from __future__ import annotations

from abc import ABC, abstractmethod
from os import makedirs, path, symlink, unlink
from typing import TYPE_CHECKING

from shellfish import batman

if TYPE_CHECKING:
    from xtyping import IterableStr, List, Tuple


class OsFsAbc(ABC):  # pragma: nocov
    """Abstract base class for OS-specific fns"""

    @staticmethod
    @abstractmethod
    def link_dir(linkpath: str, targetpath: str, *, exist_ok: bool = False) -> None: ...

    @staticmethod
    @abstractmethod
    def link_dirs(
        link_target_tuples: List[Tuple[str, str]], *, exist_ok: bool = False
    ) -> None: ...

    @staticmethod
    @abstractmethod
    def link_file(
        linkpath: str, targetpath: str, *, exist_ok: bool = False
    ) -> None: ...

    @staticmethod
    @abstractmethod
    def link_files(
        link_target_tuples: List[Tuple[str, str]], *, exist_ok: bool = False
    ) -> None: ...

    @staticmethod
    @abstractmethod
    def unlink_dir(link: str) -> None: ...

    @staticmethod
    @abstractmethod
    def unlink_dirs(links: IterableStr) -> None: ...

    @staticmethod
    @abstractmethod
    def unlink_file(link: str) -> None: ...

    @staticmethod
    @abstractmethod
    def unlink_files(links: IterableStr) -> None: ...


# =============================================================================
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# =============================================================================
#  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\  /\
# /  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \/  \
# =============================================================================
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# =============================================================================


class LIN(OsFsAbc):  # pragma: nocov
    """Linux (and Mac) shell commands/methods container"""

    @staticmethod
    def link_dir(linkpath: str, targetpath: str, *, exist_ok: bool = False) -> None:
        """Make a directory symlink

        Args:
            linkpath (str): Path to the link to be made
            targetpath (str): Path to the target of the link to be made
            exist_ok (str): Allow link to exist

        """
        try:
            symlink(targetpath, linkpath)
        except FileExistsError as fee:
            if not exist_ok:
                raise fee

    @staticmethod
    def link_dirs(
        link_target_tuples: List[Tuple[str, str]], *, exist_ok: bool = False
    ) -> None:
        """Make multiple directory symlinks

        Args:
            link_target_tuples: Iterable of tuples of the form: (link, target)
                or a dictionary mapping with key => value pairs of the form
                link => target.
            exist_ok (bool): Allow link to exist

        """
        for link, target in link_target_tuples:
            LIN.link_dir(link, target, exist_ok=exist_ok)

    @staticmethod
    def link_file(linkpath: str, targetpath: str, *, exist_ok: bool = False) -> None:
        """Make a file symlink

        Args:
            linkpath (str): Path to the link to be made
            targetpath (str): Path to the target of the link to be made
            exist_ok (bool): Allow links to already exist

        """
        makedirs(path.split(linkpath)[0], exist_ok=True)
        try:
            symlink(targetpath, linkpath)
        except FileExistsError as fee:
            if not exist_ok:
                raise fee

    @staticmethod
    def link_files(
        link_target_tuples: List[Tuple[str, str]], *, exist_ok: bool = False
    ) -> None:
        """Make multiple file symlinks

        Args:
            exist_ok (bool): Allow links to already exist
            link_target_tuples: Iterable of tuples of the form: (link, target)
                or a dictionary mapping with key => value pairs of the form
                link => target.

        """
        for link, target in link_target_tuples:
            LIN.link_file(link, target, exist_ok=exist_ok)

    @staticmethod
    def unlink_dir(link: str) -> None:
        """Unlink a directory symlink given a path to the symlink

        Args:
            link: path to the symlink

        """
        unlink(str(link))

    @staticmethod
    def unlink_dirs(links: IterableStr) -> None:
        """Unlink directory symlinks given the paths the links

        Args:
            links: Iterable of paths to links

        """
        for link in links:
            LIN.unlink_dir(link)

    @staticmethod
    def unlink_file(link: str) -> None:
        """Unlink a file symlink given a path to the symlink

        Args:
            link: path to the symlink

        """
        unlink(str(link))

    @staticmethod
    def unlink_files(links: IterableStr) -> None:
        """Unlink directory symlinks given the paths the links

        Args:
            links: Iterable of paths to links

        """
        for link in links:
            LIN.unlink_file(link)


class WIN(OsFsAbc):  # pragma: nocov
    """Windows shell commands/methods container"""

    _MAX_CMD_LENGTH: int = 8192

    @staticmethod
    def link_dir(linkpath: str, targetpath: str, *, exist_ok: bool = False) -> None:
        """Make a directory symlink

        Args:
            linkpath (str): Path to the link to be made
            targetpath (str): Path to the target of the link to be made
            exist_ok (bool): If True, do not raise an exception if the link exists

        """
        makedirs(path.split(linkpath)[0], exist_ok=True)
        try:
            symlink(targetpath, linkpath, target_is_directory=True)
        except OSError:
            batman.MKLINK(
                linkpath,
                targetpath,
                D=True,
            )

    @staticmethod
    def link_dirs(
        link_target_tuples: List[Tuple[str, str]], *, exist_ok: bool = False
    ) -> None:
        """Make multiple directory symlinks

        Args:
            link_target_tuples: Iterable of tuples of the form: (link, target)
                or a dictionary mapping with key => value pairs of the form
                link => target.
            exist_ok (bool): If True, do not raise an exception if the link(s) exist

        """
        try:
            for link, target in link_target_tuples:
                WIN.link_dir(link, target, exist_ok=exist_ok)
        except OSError:
            args = [
                batman.MKLINK_ARGS(link, target, D=True)
                for link, target in link_target_tuples
                if WIN._check_link_target_dirs(link, target)
            ]
            batman.run_cmds_as_bat_file(commands=[" ".join(el) for el in args])

    @staticmethod
    def link_file(linkpath: str, targetpath: str, *, exist_ok: bool = False) -> None:
        """Make a file symlink

        Args:
            linkpath (str): Path to the link to be made
            targetpath (str): Path to the target of the link to be made
            exist_ok (bool): If True, don't raise an exception if the link exists

        """
        try:
            symlink(targetpath, linkpath)
        except OSError:
            makedirs(path.split(linkpath)[0], exist_ok=True)
            batman.MKLINK(
                linkpath,
                targetpath,
            )

    @staticmethod
    def link_files(
        link_target_tuples: List[Tuple[str, str]], *, exist_ok: bool = False
    ) -> None:
        """Make multiple file symlinks

        Args:
            link_target_tuples: Iterable of tuples of the form: (link, target)
                or a dictionary mapping with key => value pairs of the form
                link => target.
            exist_ok (bool): If True, don't raise an exception if the link exists

        """
        try:
            for link, target in link_target_tuples:
                WIN.link_file(link, target, exist_ok=exist_ok)
        except OSError:
            link_target_tuples = list(link_target_tuples)
            _args = [
                batman.MKLINK_ARGS(link, target, D=False)
                for link, target in link_target_tuples
                if WIN._check_link_target_files(link, target)
            ]
            batman.run_cmds_as_bat_file(commands=[" ".join(el) for el in _args])

    @staticmethod
    def unlink_dir(link: str) -> None:
        """Unlink a directory symlink given a path to the symlink

        Args:
            link: path to the symlink

        """
        try:
            unlink(link)
        except OSError:
            batman.RD(link)

    @staticmethod
    def unlink_dirs(links: IterableStr) -> None:
        """Unlink directory symlinks given the paths the links

        Args:
            links: Iterable of paths to links

        """
        try:
            for link in links:
                WIN.unlink_dir(link)
        except OSError:
            batman.run_cmds_as_bat_file(
                commands=[batman.RD_ARGS(link) for link in links]
            )

    @staticmethod
    def unlink_file(link: str) -> None:
        """Unlink a file symlink given a path to the symlink

        Args:
            link (str): path to the symlink

        """
        try:
            unlink(link)
        except OSError:
            batman.DEL(link)

    @staticmethod
    def unlink_files(links: IterableStr) -> None:
        """Unlink directory symlinks given the paths the links

        Args:
            links: Iterable of paths to links

        """
        try:
            for link in links:
                WIN.unlink_file(link)
        except OSError:
            batman.run_cmds_as_bat_file(
                [batman.DEL_ARGS(link) for link in links],
            )

    @staticmethod
    def _check_link_target_files(link: str, target: str) -> bool:
        """Check for valid symbolic link to specified target file"""
        link = str(link)
        target = str(target)
        try:
            assert path.exists(target)
            makedirs(path.split(link)[0], exist_ok=True)
            return True
        except Exception:
            ...
        return False

    @staticmethod
    def _check_link_target_dirs(link: str, target: str) -> bool:
        """Check for valid symbolic link to specified target directory"""
        link = str(link)
        target = str(target)
        try:
            assert path.isdir(target)
            makedirs(path.split(link)[0], exist_ok=True)
        except Exception:
            ...
        return True
