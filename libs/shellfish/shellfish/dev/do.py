from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple, Union

from jsonbourne.pydantic import JsonBaseModel
from shellfish._types import FsPath


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
    timeout: Optional[int] = None
    verbose: bool = False
