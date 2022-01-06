import os

from xtyping import _typing as t, _typing_extensions as te, shed

include_in_all = {
    '__version__',
    'typing',
    'typing_extensions',
}
header = '''# -*- coding: utf-8 -*-
"""typing + typing_extensions + misc types/aliases"""
import typing

import typing_extensions

from xtyping._meta import __version__
'''

imports = {
    'typing': (el for el in t.__all__ if el not in te.__all__),
    'typing_extensions': te.__all__,
    'shed': shed.__all__,
}


init_all = [
    '__all__ = (',
    *[
        f"    '{el}',"
        for el in sorted({*t.__all__, *te.__all__, *shed.__all__, *include_in_all})
    ],
    ')',
]
init_parts = [
    header,
    *[f'from xtyping._typing import {el}' for el in imports['typing']],
    *[
        f'from xtyping._typing_extensions import {el}'
        for el in imports['typing_extensions']
    ],
    *[f'from xtyping.shed import {el}' for el in imports['shed']],
    *init_all,
]

with open(os.path.join('xtyping', '__init__.py'), 'w') as f:
    f.write('\n'.join(init_parts))
