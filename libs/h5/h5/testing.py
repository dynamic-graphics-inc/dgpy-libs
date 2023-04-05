"""h5.testing"""
from pathlib import Path
from typing import Union

import numpy as np

import h5

__all__ = (
    "EXPECTED_ATTRS",
    "EXPECTED_DATASETS",
    "EXPECTED_GROUPS_KEYS",
    "make_test_hdf5_file",
)

EXPECTED_DATASETS = {
    "/root_dataset": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    "/a_subgroup/a_dataset": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset": np.array(
        [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
    ),
    "/b_subgroup/b_dataset": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    "/vanilla": np.arange(100),
    "/chunked": np.arange(100) * 2,
    "/filter-gzip": np.arange(100) * 3,
    "/filter-lzf": np.arange(100) * 4,
}
EXPECTED_ATTRS = {
    "/": {
        "root_attr_str": "root_attr_value",
    },
    "/root_dataset": {
        "root_attr_float": 123.456,
        "root_attr_int": 123,
        "root_attr_list": np.array([1, 2, 3]),
        "root_attr_np_array": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        "root_attr_str": "root_attr_value",
    },
    "/a_subgroup": {"a_attr": "a_attr_value"},
    "/b_subgroup": {"b_attr": "b_attr_value"},
    "/a_subgroup/a_dataset": {"a_dataset_attr": "a_dataset_attr_value"},
    "/a_subgroup/aa_subsubgroup": {"aa_subsubgroup_attr": "aa_subsubgroup_attr_value"},
    "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset": {
        "aa_subsubgroup_dataset_attr": "aa_subsubgroup_dataset_attr_value"
    },
    "/b_subgroup/b_dataset": {"b_dataset_attr": "b_dataset_attr_value"},
    "/chunked": {"desc": "chunked-dataset"},
    "/filter-gzip": {"desc": "filter-gzip-dataset"},
    "/filter-lzf": {"desc": "filter-lzf-dataset"},
    "/vanilla": {"desc": "vanilla-dataset"},
}

EXPECTED_GROUPS_KEYS = [
    "/",
    "/a_subgroup",
    "/a_subgroup/aa_subsubgroup",
    "/b_subgroup",
]


def make_test_hdf5_file(filepath: Union[str, Path]) -> str:
    """Make test hdf5 file and return filepath"""
    with h5.File(str(filepath), mode="w") as f:
        # set root group attributes
        f.attrs["root_attr_str"] = "root_attr_value"

        root_dataset = f.create_dataset(
            "root_dataset", data=np.arange(10).reshape(2, 5)
        )
        root_dataset.attrs["root_attr_str"] = "root_attr_value"
        root_dataset.attrs["root_attr_int"] = 123
        root_dataset.attrs["root_attr_float"] = 123.456
        root_dataset.attrs["root_attr_list"] = [1, 2, 3]
        root_dataset.attrs["root_attr_np_array"] = np.arange(10).reshape(2, 5)

        a_subgrp = f.create_group("a_subgroup")
        a_subgrp.attrs["a_attr"] = "a_attr_value"
        a_dataset = a_subgrp.create_dataset(
            "a_dataset", data=np.arange(10).reshape(2, 5)
        )
        a_dataset.attrs["a_dataset_attr"] = "a_dataset_attr_value"

        b_subgrp = f.create_group("b_subgroup")
        b_subgrp.attrs["b_attr"] = "b_attr_value"

        b_dataset = b_subgrp.create_dataset(
            "b_dataset", data=np.arange(10).reshape(2, 5)
        )

        b_dataset.attrs["b_dataset_attr"] = "b_dataset_attr_value"

        aa_subsubgrp = a_subgrp.create_group("aa_subsubgroup")
        aa_subsubgrp.attrs["aa_subsubgroup_attr"] = "aa_subsubgroup_attr_value"
        aa_subsbugrp_dataset = aa_subsubgrp.create_dataset(
            "aa_subsubgroup_dataset", data=np.arange(10).reshape(2, 5)
        )
        aa_subsbugrp_dataset.attrs[
            "aa_subsubgroup_dataset_attr"
        ] = "aa_subsubgroup_dataset_attr_value"

        dset_vanilla = f.create_dataset(
            "vanilla", shape=(100,), dtype="i", data=np.arange(100)
        )
        dset_vanilla.attrs["desc"] = "vanilla-dataset"
        dset_chunked = f.create_dataset(
            "chunked", (100,), dtype="i", chunks=(10,), data=np.arange(100) * 2
        )
        dset_chunked.attrs["desc"] = "chunked-dataset"
        dset_filter_gzip = f.create_dataset(
            "filter-gzip",
            (100,),
            dtype="i",
            chunks=(10,),
            compression="gzip",
            compression_opts=5,
            data=np.arange(100) * 3,
        )
        dset_filter_gzip.attrs["desc"] = "filter-gzip-dataset"
        dset_filter_lzf = f.create_dataset(
            "filter-lzf",
            (100,),
            dtype="i",
            chunks=(10,),
            compression="lzf",
            data=np.arange(100) * 4,
        )
        dset_filter_lzf.attrs["desc"] = "filter-lzf-dataset"
    return str(filepath)
