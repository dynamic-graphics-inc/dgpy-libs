from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union

from typing_extensions import TypedDict

from jsonbourne.pydantic import JsonBaseModel

if TYPE_CHECKING:
    from shellfish._types import FsPath


class DoDict(TypedDict):
    """Do dictionary"""

    args: Union[List[str], Tuple[str, ...]]
    check: bool
    cwd: Optional[FsPath]
    dryrun: bool
    env: Optional[Dict[str, str]]
    extenv: bool
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]]
    shell: bool
    tee: bool
    timeout: Optional[Union[float, int]]
    verbose: bool


class Do(JsonBaseModel):
    """PRun => 'ProcessRun' for finished processes"""

    args: Union[List[str], Tuple[str, ...]]
    check: bool = False
    cwd: Optional[FsPath] = None
    dryrun: bool = False
    env: Optional[Dict[str, str]] = None
    extenv: bool = True
    ok_code: Union[int, List[int], Tuple[int, ...], Set[int]] = (0,)
    shell: bool = False
    tee: bool = False
    timeout: Optional[Union[float, int]] = None
    verbose: bool = False

    def typed_dict(self) -> DoDict:
        return {
            "args": self.args,
            "check": self.check,
            "cwd": self.cwd,
            "dryrun": self.dryrun,
            "env": self.env,
            "extenv": self.extenv,
            "ok_code": self.ok_code,
            "shell": self.shell,
            "tee": self.tee,
            "timeout": self.timeout,
            "verbose": self.verbose,
        }
