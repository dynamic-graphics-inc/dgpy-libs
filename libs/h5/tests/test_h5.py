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
    "/a_subgroup",
    "/a_subgroup/a_dataset",
    "/a_subgroup/aa_subsubgroup",
    "/a_subgroup/aa_subsubgroup/aa_subsubgroup_dataset",
    "/b_subgroup",
    "/b_subgroup/b_dataset",
]


def dummy_hdf5_file(filepath: str):
    with h5py.File(filepath, mode="w") as f:
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


def test_h5_attrs_gen(tmpdir):
    filepath = tmpdir.join("test.h5").strpath
    print(filepath)
    dummy_hdf5_file(filepath)
    expected = {**EXPECTED_ATTRS}

    attrs_gen_dictionary = dict(h5.attrs_gen(filepath))
    assert attrs_gen_dictionary is not None
    attrs_dictionary = h5.attrs_dict(filepath)
    print(attrs_dictionary)
    attrs_dictionary_dictionary = {k: {**v} for k, v in attrs_dictionary.items()}
    print(attrs_dictionary_dictionary)

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
        print(attrs_dictionary)
        attrs_dictionary_dictionary = {k: {**v} for k, v in attrs_dictionary.items()}
        print(attrs_dictionary_dictionary)

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
        datasets_dict_from_file = dict(h5.datasets_gen(f))
        print(datasets_dict_from_file)

    datasets_dict_from_filepath = {k: v[()] for k, v in h5.datasets_gen(filepath)}
    assert datasets_dict_from_filepath is not None
    assert sorted(EXPECTED_DATASETS.keys()) == sorted(
        datasets_dict_from_filepath.keys()
    )
    for k, v in datasets_dict_from_filepath.items():
        print(v, EXPECTED_DATASETS[k])
        assert np.array_equal(v, EXPECTED_DATASETS[k])

    with h5py.File(filepath, mode="r") as f:
        datasets_dict_from_file_obj = h5.datasets_dict(f)
        assert datasets_dict_from_file_obj is not None
        for k, v in datasets_dict_from_file_obj.items():
            assert np.array_equal(v, EXPECTED_DATASETS[k])

    datasets_dict_from_filepath = h5.datasets_dict(filepath)
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
        print(groups_dict_from_file)

        groups_dict_from_filepath = dict(h5.groups_gen(filepath))
        assert groups_dict_from_filepath is not None
        assert EXPECTED_GROUPS_KEYS == sorted(groups_dict_from_filepath.keys())
        print(groups_dict_from_filepath.keys())
        assert sorted(groups_dict_from_filepath.keys()) == sorted(
            groups_dict_from_file.keys()
        )
