import numpy as np
import pytest

import h5

from h5._info import DatasetInfo, FileInfo, GroupInfo
from h5.testing import make_test_hdf5_file

array = np.array

h5_test_file_info = FileInfo(
    groups={
        "a_subgroup": GroupInfo(
            groups={
                "aa_subsubgroup": GroupInfo(
                    groups={},
                    attrs={"aa_subsubgroup_attr": "aa_subsubgroup_attr_value"},
                    datasets={
                        "aa_subsubgroup_dataset": DatasetInfo(
                            key="/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset",
                            attrs={
                                "aa_subsubgroup_dataset_attr": "aa_subsubgroup_dataset_attr_value"
                            },
                            shape=(2, 5),
                            ndim=2,
                            dtype="int64",
                            dtype_str="<i8",
                            size=10,
                            nbytes=80,
                            h5type="dataset",
                            compression=None,
                            compression_opts=None,
                            maxshape=(2, 5),
                            chunks=None,
                        )
                    },
                    key="/a_subgroup/aa_subsubgroup",
                    h5type="group",
                )
            },
            attrs={"a_attr": "a_attr_value"},
            datasets={
                "a_dataset": DatasetInfo(
                    key="/a_subgroup/a_dataset",
                    attrs={"a_dataset_attr": "a_dataset_attr_value"},
                    shape=(2, 5),
                    ndim=2,
                    dtype="int64",
                    dtype_str="<i8",
                    size=10,
                    nbytes=80,
                    h5type="dataset",
                    compression=None,
                    compression_opts=None,
                    maxshape=(2, 5),
                    chunks=None,
                )
            },
            key="/a_subgroup",
            h5type="group",
        ),
        "b_subgroup": GroupInfo(
            groups={},
            attrs={"b_attr": "b_attr_value"},
            datasets={
                "b_dataset": DatasetInfo(
                    key="/b_subgroup/b_dataset",
                    attrs={"b_dataset_attr": "b_dataset_attr_value"},
                    shape=(2, 5),
                    ndim=2,
                    dtype="int64",
                    dtype_str="<i8",
                    size=10,
                    nbytes=80,
                    h5type="dataset",
                    compression=None,
                    compression_opts=None,
                    maxshape=(2, 5),
                    chunks=None,
                )
            },
            key="/b_subgroup",
            h5type="group",
        ),
    },
    attrs={"root_attr_str": "root_attr_value"},
    datasets={
        "chunked": DatasetInfo(
            key="/chunked",
            attrs={"desc": "chunked-dataset"},
            shape=(100,),
            ndim=1,
            dtype="int64",
            dtype_str="<i8",
            size=100,
            nbytes=800,
            h5type="dataset",
            compression=None,
            compression_opts=None,
            maxshape=(100,),
            chunks=(10,),
        ),
        "filter-gzip": DatasetInfo(
            key="/filter-gzip",
            attrs={"desc": "filter-gzip-dataset"},
            shape=(100,),
            ndim=1,
            dtype="int64",
            dtype_str="<i8",
            size=100,
            nbytes=800,
            h5type="dataset",
            compression="gzip",
            compression_opts=5,
            maxshape=(100,),
            chunks=(10,),
        ),
        "filter-lzf": DatasetInfo(
            key="/filter-lzf",
            attrs={"desc": "filter-lzf-dataset"},
            shape=(100,),
            ndim=1,
            dtype="int64",
            dtype_str="<i8",
            size=100,
            nbytes=800,
            h5type="dataset",
            compression="lzf",
            compression_opts=None,
            maxshape=(100,),
            chunks=(10,),
        ),
        "root_dataset": DatasetInfo(
            key="/root_dataset",
            attrs={
                "root_attr_float": 123.456,
                "root_attr_int": 123,
                "root_attr_list": array([1, 2, 3]),
                "root_attr_np_array": array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
                "root_attr_str": "root_attr_value",
            },
            shape=(2, 5),
            ndim=2,
            dtype="int64",
            dtype_str="<i8",
            size=10,
            nbytes=80,
            h5type="dataset",
            compression=None,
            compression_opts=None,
            maxshape=(2, 5),
            chunks=None,
        ),
        "vanilla": DatasetInfo(
            key="/vanilla",
            attrs={"desc": "vanilla-dataset"},
            shape=(100,),
            ndim=1,
            dtype="int64",
            dtype_str="<i8",
            size=100,
            nbytes=800,
            h5type="dataset",
            compression=None,
            compression_opts=None,
            maxshape=(100,),
            chunks=None,
        ),
    },
    fspath="test.h5",
    fssize=20526,
    key="/",
    h5type="file",
)


def test_h5_info_objects(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    make_test_hdf5_file(filepath)

    file_info = h5.info(filepath)

    assert isinstance(file_info, FileInfo)
    file_info.fspath = "test.h5"
    assert file_info.dict(attributes=False) == h5_test_file_info.dict(attributes=False)

    assert "vanilla" in file_info.datasets
    assert "vanilla" in file_info


class TestH5FileInfoObj:
    def test_contains(self):
        assert "vanilla" in h5_test_file_info.datasets
        assert "vanilla" in h5_test_file_info

        assert "root_dataset" in h5_test_file_info.datasets
        assert "root_dataset" in h5_test_file_info

    def test_len(self):
        assert len(h5_test_file_info) == len(h5_test_file_info.datasets) + len(
            h5_test_file_info.groups
        )

    def test_getitem(self):
        assert h5_test_file_info["vanilla"] == h5_test_file_info.datasets["vanilla"]
        assert (
            h5_test_file_info["root_dataset"]
            == h5_test_file_info.datasets["root_dataset"]
        )

    def test_getitem_raises(self):
        with pytest.raises(KeyError):
            h5_test_file_info.get("nonexistent")

    def test_get(self):
        vanilla_dataset = h5_test_file_info.datasets["vanilla"]
        assert h5_test_file_info.get("vanilla") == vanilla_dataset
        assert (
            h5_test_file_info.get("nonexistent", default=vanilla_dataset)
            is vanilla_dataset
        )

        with pytest.raises(TypeError):
            assert h5_test_file_info.get("nonexistent", default=123)  # type: ignore[arg-type]

    def test_dump_gen(self):
        list_dump_gen = list(h5_test_file_info.dump_gen(attributes=False))
        dump_gen_expected = [
            {
                "h5type": "file",
                "fspath": "test.h5",
                "fssize": 20526,
                "key": "/",
                "attrs": {"root_attr_str": "root_attr_value"},
                "groups": ["/a_subgroup", "/b_subgroup"],
                "datasets": [
                    "/chunked",
                    "/filter-gzip",
                    "/filter-lzf",
                    "/root_dataset",
                    "/vanilla",
                ],
            },
            {
                "h5type": "group",
                "key": "/a_subgroup",
                "attrs": {"a_attr": "a_attr_value"},
                "groups": ["/a_subgroup/aa_subsubgroup"],
                "datasets": ["/a_subgroup/a_dataset"],
            },
            {
                "h5type": "group",
                "key": "/a_subgroup/aa_subsubgroup",
                "attrs": {"aa_subsubgroup_attr": "aa_subsubgroup_attr_value"},
                "groups": [],
                "datasets": ["/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset"],
            },
            {
                "h5type": "dataset",
                "attrs": {
                    "aa_subsubgroup_dataset_attr": "aa_subsubgroup_dataset_attr_value"
                },
                "key": "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset",
                "shape": (2, 5),
                "ndim": 2,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 10,
                "nbytes": 80,
                "compression": None,
                "compression_opts": None,
                "maxshape": (2, 5),
                "chunks": None,
            },
            {
                "h5type": "dataset",
                "attrs": {"a_dataset_attr": "a_dataset_attr_value"},
                "key": "/a_subgroup/a_dataset",
                "shape": (2, 5),
                "ndim": 2,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 10,
                "nbytes": 80,
                "compression": None,
                "compression_opts": None,
                "maxshape": (2, 5),
                "chunks": None,
            },
            {
                "h5type": "group",
                "key": "/b_subgroup",
                "attrs": {"b_attr": "b_attr_value"},
                "groups": [],
                "datasets": ["/b_subgroup/b_dataset"],
            },
            {
                "h5type": "dataset",
                "attrs": {"b_dataset_attr": "b_dataset_attr_value"},
                "key": "/b_subgroup/b_dataset",
                "shape": (2, 5),
                "ndim": 2,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 10,
                "nbytes": 80,
                "compression": None,
                "compression_opts": None,
                "maxshape": (2, 5),
                "chunks": None,
            },
            {
                "h5type": "dataset",
                "attrs": {"desc": "chunked-dataset"},
                "key": "/chunked",
                "shape": (100,),
                "ndim": 1,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 100,
                "nbytes": 800,
                "compression": None,
                "compression_opts": None,
                "maxshape": (100,),
                "chunks": (10,),
            },
            {
                "h5type": "dataset",
                "attrs": {"desc": "filter-gzip-dataset"},
                "key": "/filter-gzip",
                "shape": (100,),
                "ndim": 1,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 100,
                "nbytes": 800,
                "compression": "gzip",
                "compression_opts": 5,
                "maxshape": (100,),
                "chunks": (10,),
            },
            {
                "h5type": "dataset",
                "attrs": {"desc": "filter-lzf-dataset"},
                "key": "/filter-lzf",
                "shape": (100,),
                "ndim": 1,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 100,
                "nbytes": 800,
                "compression": "lzf",
                "compression_opts": None,
                "maxshape": (100,),
                "chunks": (10,),
            },
            {
                "h5type": "dataset",
                "attrs": {
                    "root_attr_float": 123.456,
                    "root_attr_int": 123,
                    "root_attr_list": np.array([1, 2, 3]),
                    "root_attr_np_array": np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
                    "root_attr_str": "root_attr_value",
                },
                "key": "/root_dataset",
                "shape": (2, 5),
                "ndim": 2,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 10,
                "nbytes": 80,
                "compression": None,
                "compression_opts": None,
                "maxshape": (2, 5),
                "chunks": None,
            },
            {
                "h5type": "dataset",
                "attrs": {"desc": "vanilla-dataset"},
                "key": "/vanilla",
                "shape": (100,),
                "ndim": 1,
                "dtype": "int64",
                "dtype_str": "<i8",
                "size": 100,
                "nbytes": 800,
                "compression": None,
                "compression_opts": None,
                "maxshape": (100,),
                "chunks": None,
            },
        ]
        dump_gen_expected_no_attrs = [
            {k: v if k != "attrs" else {} for k, v in d.items()}  # type: ignore[attr-defined]
            for d in dump_gen_expected
        ]
        assert list_dump_gen == dump_gen_expected_no_attrs

    def test_setitem_type_error(self):
        with pytest.raises(TypeError):
            h5_test_file_info["vanilla"] = 123  # type: ignore[assignment]
