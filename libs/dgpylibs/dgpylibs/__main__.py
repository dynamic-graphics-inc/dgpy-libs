# -*- coding: utf-8 -*-
"""pkg entry ~ `python -m dgpylibs`"""
import sys

from dgpylibs import DgpyLibsMetadataDict, dgpylibs_metadata

try:
    from rich import print_json

    def print_dgpy_metadata(
        data: DgpyLibsMetadataDict,
    ) -> None:
        print_json(data=data, indent=2)

except ImportError:
    import json

    def print_dgpy_metadata(
        data: DgpyLibsMetadataDict,
    ) -> None:
        sys.stdout.write(json.dumps(data, indent=2))


def main() -> None:
    print_dgpy_metadata(dgpylibs_metadata.asdict())


if __name__ == "__main__":
    main()
