# ruff: noqa: F821
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requires


@requires.requires("import somelibrary as sl")
def frobulize(inputs: list[str]) -> list[str]:
    return sl.frobulize(inputs)  # type: ignore[name-defined, no-any-return]


@requires.requires("import somelibrary as sl")
@requires.requires("import some_other_lib as sol")  # sol=shit out o luck?
def frobulize_multiple_requirements(inputs: list[str]) -> tuple[Any, ...]:
    return (sl.frobulize(sl.frobulize(inputs)), sol.do_stuff())  # type: ignore[name-defined]


if TYPE_CHECKING:
    from typing import reveal_type

    r1 = requires.Requirement(_import="somelibrary", _as="sl")
    r2 = requires.Requirement(_import="some_other_lib", _as="sol")

    @r1
    def frobulize_v2(inputs: list[str]) -> list[str]:
        return sl.frobulize(inputs)  # type: ignore[name-defined, no-any-return]

    @r1
    @r1
    def frobulize_multiple_requirements_v2(inputs: list[str]) -> tuple[Any, ...]:
        return (sl.frobulize(sl.frobulize(inputs)), sol.do_stuff())  # type: ignore[name-defined]

    reveal_type(frobulize)
    reveal_type(frobulize_multiple_requirements)
    reveal_type(frobulize_v2)
    reveal_type(frobulize_multiple_requirements_v2)
