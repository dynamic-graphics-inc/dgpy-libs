from os import listdir, path

import dgpydev

PWD = path.split(path.abspath(__file__))[0]
REPO_ROOT = path.split(PWD)[0]


def test_libs_listing():
    libs_dirs = tuple(sorted(listdir(path.join(REPO_ROOT, "libs"))))
    assert libs_dirs == dgpydev.DGPY_LIBS
