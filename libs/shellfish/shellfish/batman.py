# -*- coding: utf-8 -*-
"""batman = bat/cmd windows utils"""
from __future__ import annotations

import tempfile

from os import fspath as _fspath, getenv as _getenv
from pathlib import Path
from shutil import which
from subprocess import CompletedProcess, run
from typing import Sequence

from xtyping import AnyStr, FsPath, Tuple, Union

MAX_CMD_LENGTH: int = 8192

WIN_DEFAULT_PATHEXT: str = ".COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC"


def pathext() -> Tuple[str, ...]:
    pathext_source = _getenv("PATHEXT") or WIN_DEFAULT_PATHEXT
    return tuple(pathext_source.split(";"))


def bat(
    fspath: FsPath, *, check: bool = False, text: bool = True, shell: bool = False
) -> CompletedProcess[AnyStr]:
    """Run a bat file"""
    bat_filepath = which(fspath)
    if bat_filepath is None:
        fspath_obj = Path(fspath)
        if not fspath_obj.exists():
            raise FileNotFoundError(fspath)
    else:
        fspath_obj = Path(bat_filepath)

    _args = [str(fspath)] if shell else ["cmd", "/c", _fspath(fspath_obj)]
    return run(
        args=_args,
        capture_output=True,
        shell=shell,
        text=text,
        check=check,
        cwd=fspath_obj.parent,
    )


def run_cmd(cmd: str, *, text: bool = True) -> CompletedProcess[AnyStr]:
    return run(cmd, check=True, capture_output=True, text=text, shell=True)


def run_cmds(cmds: Sequence[str]) -> CompletedProcess[AnyStr]:
    _commands = ["CALL " + cmd for cmd in cmds]
    if len(_commands) == 0:
        raise ValueError("no commands given")
    if len(_commands) == 1:
        return run_cmd(_commands[0])
    return run_cmds_as_bat_file(_commands)


def run_cmds_as_bat_file(
    commands: Sequence[Union[Tuple[str, ...], str]], *, text: bool = True
) -> CompletedProcess[AnyStr]:
    if len(commands) == 0:
        raise ValueError("no commands given")
    _commands = [
        "CALL " + cmd
        for cmd in (el if isinstance(el, str) else " ".join(el) for el in commands)
    ]
    with tempfile.TemporaryDirectory() as tmpdirname:
        bat_filepath = Path(tmpdirname) / "f.bat"
        with bat_filepath.open(mode="w", newline="\r\n") as f:
            bat_file_str = "\r\n".join(_commands)
            f.write(bat_file_str)
        return bat(bat_filepath, text=text)


def MKLINK_OPT(D: bool = False, H: bool = False, J: bool = False) -> Union[str, None]:
    # Check that only one of D, H, J is True
    if sum((D, H, J)) > 1:
        raise ValueError(f"Only one of D, H, J can be True.  Got {D}, {H}, {J}")
    if D:
        return "/D"
    if H:
        return "/H"
    if J:
        return "/J"
    return None


def MKLINK_ARGS(
    link: FsPath, target: FsPath, *, D: bool = False, H: bool = False, J: bool = False
) -> Union[Tuple[str, str, str, str], Tuple[str, str, str]]:
    link_path = Path(link).absolute()
    target_path = Path(target).absolute()
    mklink_opt = MKLINK_OPT(D=D, H=H, J=J)
    if mklink_opt is None:
        return "MKLINK", _fspath(link_path), _fspath(target_path)
    return "MKLINK", mklink_opt, _fspath(link_path), _fspath(target_path)


_MKLINK = MKLINK_ARGS


def MKLINK(
    link: FsPath,
    target: FsPath,
    *,
    D: bool = False,
    H: bool = False,
    J: bool = False,
    check: bool = False,
) -> CompletedProcess[str]:
    """
    Creates a symbolic link.

    Returns:
        pass

    Output of `MKLINK /?`:
        ```
        MKLINK [[/D] | [/H] | [/J]] Link Target

                /D      Creates a directory symbolic link.  Default is a file
                        symbolic link.
                /H      Creates a hard link instead of a symbolic link.
                /J      Creates a Directory Junction.
                Link    Specifies the new symbolic link name.
                Target  Specifies the path (relative or absolute) that the new link
                        refers to.

        ```

    """
    link = _fspath(Path(link))
    target = _fspath(Path(target))
    _args = _MKLINK(link, target, D=D, H=H, J=J)
    return run(args=_args, check=check, capture_output=True, text=True, shell=True)


def RD_ARGS(
    fspath: FsPath,
    *,
    S: bool = False,
    Q: bool = False,
    R: bool = False,
    P: bool = False,
    F: bool = False,
    X: bool = False,
    Y: bool = False,
    Z: bool = False,
    A: bool = False,
) -> Tuple[str, ...]:
    opts = (
        "/S" if S else None,
        "/Q" if Q else None,
        "/R" if R else None,
        "/P" if P else None,
        "/F" if F else None,
        "/X" if X else None,
        "/Y" if Y else None,
        "/Z" if Z else None,
        "/A" if A else None,
    )
    return (
        "RD",
        *(el for el in opts if el is not None),
        _fspath(Path(fspath).absolute()),
    )


_RD = RD_ARGS


def RD(
    fspath: FsPath,
    *,
    S: bool = False,
    Q: bool = False,
    R: bool = False,
    P: bool = False,
    F: bool = False,
    X: bool = False,
    Y: bool = False,
    Z: bool = False,
    A: bool = False,
    check: bool = False,
) -> CompletedProcess[str]:
    """
    Removes a directory.

    Returns:
        pass


    Output of `RD /?`:
        ```
        RD [/S] [/Q] [/R] [/P] [/F] [/X] [/Y] [/Z] [/A] [Drive:]Path

                /S      Recursively removes subdirectories and files.
                /Q      Quiet.  Do not display progress messages.
                /R      Recursively removes subdirectories and files.
                /P      Prompts before each removal.
                /F      Do not display confirmation messages.
                /X      Do not display confirmation messages.
                /Y      Do not display confirmation messages.
                /Z      Do not display confirmation messages.
                /A      Do not display confirmation messages.
                Drive:  Specifies the drive or root directory of the path.
                Path    Specifies the path to be removed.

        ```

    """
    _args = _RD(fspath, S=S, Q=Q, R=R, P=P, F=F, X=X, Y=Y, Z=Z, A=A)
    return run(args=_args, check=check, capture_output=True, text=True, shell=True)


def DEL_ARGS(fspath: FsPath) -> Tuple[str, str]:
    path_obj = Path(fspath).absolute()
    return (
        "DEL",
        _fspath(path_obj),
    )


_DEL = DEL_ARGS


def DEL(fspath: FsPath, *, check: bool = False) -> CompletedProcess[str]:
    return run(
        args=("DEL", _fspath(Path(fspath))),
        check=check,
        capture_output=True,
        text=True,
        shell=True,
    )
