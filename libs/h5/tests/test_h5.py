import os

import h5py
import numpy as np

from numpy import array

import h5

EXPECTED_DATASETS = {
    "/root_dataset": array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    "/a_subgroup/a_dataset": array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
    "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset": array(
        [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
    ),
    "/b_subgroup/b_dataset": array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
}
EXPECTED_ATTRS = {
    "/": {
        "root_attr_str": "root_attr_value",
    },
    "/a_subgroup": {"a_attr": "a_attr_value"},
    "/b_subgroup": {"b_attr": "b_attr_value"},
    "/root_dataset": {
        "root_attr_float": 123.456,
        "root_attr_int": 123,
        "root_attr_list": array([1, 2, 3]),
        "root_attr_np_array": array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]),
        "root_attr_str": "root_attr_value",
    },
    "/a_subgroup/a_dataset": {"a_dataset_attr": "a_dataset_attr_value"},
    "/a_subgroup/aa_subsubgroup": {"aa_subsubgroup_attr": "aa_subsubgroup_attr_value"},
    "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset": {
        "aa_subsubgroup_dataset_attr": "aa_subsubgroup_dataset_attr_value"
    },
    "/b_subgroup/b_dataset": {"b_dataset_attr": "b_dataset_attr_value"},
}

EXPECTED_GROUPS_KEYS = [
    "/",
    "/a_subgroup",
    "/a_subgroup/aa_subsubgroup",
    "/b_subgroup",
]


def dummy_hdf5_file(filepath: str) -> str:
    with h5py.File(filepath, mode="w") as f:
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
    return filepath


def test_is_hdf5_file(tmpdir):
    os.chdir(tmpdir.strpath)
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)

    with open("not-a-file.h5", "w") as f:
        f.write("not a hdf5 file")
    assert not h5.is_hdf5("not-a-file.h5")


def test_type_guards(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)

    assert h5.is_hdf5(filepath)

    with h5py.File(filepath, mode="r") as f:
        assert h5.is_fspath(filepath)
        assert not h5.is_fspath(f)

        assert h5.is_file(f)

        # test that file is group
        assert h5.is_group(f)

        assert h5.is_group_like(f)
        assert not h5.is_group_like(f.get("root_dataset"))
        assert h5.is_group(f.get("a_subgroup"))
        assert h5.is_group(f.get("a_subgroup/aa_subsubgroup"))

        assert not h5.is_group(f.get("root_dataset"))
        assert h5.is_dataset(f.get("root_dataset"))
        assert not h5.is_dataset(f.get("a_subgroup"))
        assert not h5.is_dataset(f.get("a_subgroup/aa_subsubgroup"))


def test_h5_iter(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)
    with h5py.File(filepath, mode="r") as f:
        iter_result = list(h5.h5iter(f))
        iter_result_keys = [k for k, v in iter_result]
        assert sorted(iter_result_keys) == sorted(
            [*EXPECTED_DATASETS.keys(), *EXPECTED_GROUPS_KEYS]
        )

        list_o_keys = h5.keys_list(f)
        assert sorted(list_o_keys) == sorted(
            [*EXPECTED_DATASETS.keys(), *EXPECTED_GROUPS_KEYS]
        )

        list_o_group_keys = h5.groups_keys_list(f)
        assert sorted(list_o_group_keys) == sorted(EXPECTED_GROUPS_KEYS)

        list_o_dataset_keys = h5.datasets_keys_list(f)
        assert sorted(list_o_dataset_keys) == sorted(EXPECTED_DATASETS.keys())

        assert sorted(h5.h5py_obj_keys_gen(f)) == sorted(list_o_keys)


def test_h5_iter_filepath(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)
    iter_result = list(h5.h5iter(filepath))
    iter_result_keys = [k for k, v in iter_result]
    assert sorted(iter_result_keys) == sorted(
        [*EXPECTED_DATASETS.keys(), *EXPECTED_GROUPS_KEYS]
    )

    list_o_keys = h5.keys_list(filepath)
    assert sorted(list_o_keys) == sorted(
        [*EXPECTED_DATASETS.keys(), *EXPECTED_GROUPS_KEYS]
    )

    list_o_group_keys = h5.groups_keys_list(filepath)
    assert sorted(list_o_group_keys) == sorted(EXPECTED_GROUPS_KEYS)

    list_o_dataset_keys = h5.datasets_keys_list(filepath)
    assert sorted(list_o_dataset_keys) == sorted(EXPECTED_DATASETS.keys())


def test_main():
    from h5.__main__ import main

    main()


def test_h5_attrs_gen(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)
    expected = {**EXPECTED_ATTRS}

    attrs_gen_dictionary = dict(h5.h5_attrs_gen(filepath))
    assert attrs_gen_dictionary is not None
    attrs_dictionary = h5.h5_attrs_dict(filepath)
    attrs_dictionary_dictionary = {k: {**v} for k, v in attrs_dictionary.items()}

    root_dataset_attrs = attrs_dictionary_dictionary.pop("/root_dataset")
    expected_root_dataset_attrs = expected.pop("/root_dataset")

    for k, v in root_dataset_attrs.items():
        if isinstance(v, np.ndarray):
            assert np.array_equal(v, expected_root_dataset_attrs[k])
        else:
            assert v == expected_root_dataset_attrs[k]

    assert attrs_dictionary_dictionary == expected


def test_h5_attrs_gen_from_file_obj(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)
    expected = {**EXPECTED_ATTRS}

    with h5py.File(filepath, mode="r") as f:
        attrs_gen_dictionary = dict(h5.attrs_gen(f))
        assert attrs_gen_dictionary is not None
        attrs_dictionary = h5.attrs_dict(f)
        attrs_dictionary_dictionary = {k: {**v} for k, v in attrs_dictionary.items()}

        root_dataset_attrs = attrs_dictionary_dictionary.pop("/root_dataset")
        expected_root_dataset_attrs = expected.pop("/root_dataset")

        for k, v in root_dataset_attrs.items():
            if isinstance(v, np.ndarray):
                assert np.array_equal(v, expected_root_dataset_attrs[k])
            else:
                assert v == expected_root_dataset_attrs[k]

        assert attrs_dictionary_dictionary == expected


def test_h5_dataset_gen(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    filepath = dummy_hdf5_file(filepath)
    with h5py.File(filepath, mode="r") as f:
        dict(h5.datasets_gen(f))

    datasets_dict_from_filepath = {k: v[()] for k, v in h5.datasets_gen(filepath)}
    assert datasets_dict_from_filepath is not None
    assert sorted(EXPECTED_DATASETS.keys()) == sorted(
        datasets_dict_from_filepath.keys()
    )
    for k, v in datasets_dict_from_filepath.items():
        assert np.array_equal(v, EXPECTED_DATASETS[k])

    with h5py.File(filepath, mode="r") as f:
        datasets_dict_from_file_obj = h5.datasets_dict(f)
        assert datasets_dict_from_file_obj is not None
        for k, v in datasets_dict_from_file_obj.items():
            assert np.array_equal(v, EXPECTED_DATASETS[k])

    datasets_dict_from_filepath = h5.h5_datasets_dict(filepath)
    for k, v in datasets_dict_from_filepath.items():
        assert np.array_equal(v, EXPECTED_DATASETS[k])

    for h5path, ds in h5.h5_datasets_gen(filepath):
        arr = np.array(ds)
        assert np.array_equal(arr, EXPECTED_DATASETS[h5path])


def test_h5_groups_gen(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    filepath = dummy_hdf5_file(filepath)
    with h5py.File(filepath, mode="r") as f:
        groups_dict_from_file = dict(h5.groups_gen(f))

        groups_dict_from_filepath = dict(h5.groups_gen(filepath))
        assert groups_dict_from_filepath is not None
        assert EXPECTED_GROUPS_KEYS == sorted(groups_dict_from_filepath.keys())
        assert sorted(groups_dict_from_filepath.keys()) == sorted(
            groups_dict_from_file.keys()
        )


def test_no_repeated_keys(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    dummy_hdf5_file(filepath)
    with h5py.File(filepath, mode="r") as f:
        keys = set()
        for k in h5.h5py_obj_keys_gen(f):
            if k in keys:
                raise ValueError(f"Repeated key {k}")
            else:
                keys.add(k)
