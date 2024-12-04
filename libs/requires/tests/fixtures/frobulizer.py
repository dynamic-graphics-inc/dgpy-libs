from typing import Any, List, Tuple

from requires import requires


@requires("import somelibrary as sl")
def frobulize(inputs: List[str]) -> List[str]:
    return sl.frobulize(inputs)  # noqa


@requires("import somelibrary as sl")
@requires("import some_other_lib as sol")  # sol=shit out o luck?
def frobulize_multiple_requirments(inputs: List[str]) -> Tuple[Any, ...]:
    return (sl.frobulize(sl.frobulize(inputs)), sol.do_stuff())  # noqa
