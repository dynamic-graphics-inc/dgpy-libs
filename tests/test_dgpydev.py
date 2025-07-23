from os import listdir, path

import dgpydev

PWD = path.split(path.abspath(__file__))[0]
REPO_ROOT = path.split(PWD)[0]


def test_libs_listing() -> None:
    libs_dir = path.join(REPO_ROOT, "libs")
    if not path.isdir(libs_dir):
        raise AssertionError("libs dir not found", libs_dir)
    libs_dirs = tuple(sorted(listdir(libs_dir)))
    if libs_dirs != dgpydev.DGPY_LIBS:
        raise AssertionError(
            "libs dir listing doesn't match", libs_dirs, dgpydev.DGPY_LIBS
        )
