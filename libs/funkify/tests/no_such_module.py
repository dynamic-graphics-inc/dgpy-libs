# -*- coding: utf-8 -*-
import funkify


def main() -> int:
    return 123


funkify(main, key="no_such_module")  # type: ignore[operator]
