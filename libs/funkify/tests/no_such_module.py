# -*- coding: utf-8 -*-
from __future__ import annotations

import funkify


def main() -> int:
    return 123


funkify(main, key="no_such_module")  # type: ignore[operator]
