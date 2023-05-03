import os

from pathlib import Path

import h5py
import numpy as np

import h5

from h5.testing import (
    EXPECTED_ATTRS,
    EXPECTED_DATASETS,
    EXPECTED_GROUPS_KEYS,
    make_test_hdf5_file,
)


def test_is_hdf5_file(tmp_path: Path) -> None:
    os.chdir(tmp_path)
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)

    with open("not-a-file.h5", "w") as f:
        f.write("not a hdf5 file")
    assert not h5.is_hdf5("not-a-file.h5")


def test_type_guards(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)

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


def test_as_h5_obj(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)
    assert h5.is_file(h5.as_h5py_obj(filepath))
    with h5.File(filepath, mode="r") as f:
        assert h5.is_file(h5.as_h5py_obj(f))
        assert h5.is_group(h5.as_h5py_obj(f))


def test_h5_iter(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)
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


def test_h5_iter_filepath(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)
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


def test_main() -> None:
    from h5.__main__ import main

    main(h5cli=False)


def test_h5_attrs_gen(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)
    expected = {**EXPECTED_ATTRS}

    attrs_gen_dictionary = dict(h5.attrs_gen(filepath))
    assert attrs_gen_dictionary is not None
    attrs_dictionary = h5.attrs_dict(filepath)
    attrs_dictionary_dictionary = {k: {**v} for k, v in attrs_dictionary.items()}

    root_dataset_attrs = attrs_dictionary_dictionary.pop("/root_dataset")
    expected_root_dataset_attrs = expected.pop("/root_dataset")

    for k, v in root_dataset_attrs.items():
        if isinstance(v, np.ndarray):
            assert np.array_equal(v, expected_root_dataset_attrs[k])
        else:
            assert v == expected_root_dataset_attrs[k]

    assert attrs_dictionary_dictionary == expected


def test_h5_attrs_gen_from_file_obj(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)
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


def test_h5_dataset_gen(tmp_path: Path) -> None:
    _filepath = tmp_path / "test.h5"
    filepath = make_test_hdf5_file(_filepath)
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

    datasets_dict_from_filepath = h5.datasets_dict(filepath)
    for k, v in datasets_dict_from_filepath.items():
        assert np.array_equal(v, EXPECTED_DATASETS[k])

    for h5path, ds in h5.datasets_gen(filepath):
        arr = np.array(ds)
        assert np.array_equal(arr, EXPECTED_DATASETS[h5path])


def test_h5_groups_gen(tmp_path: Path) -> None:
    _filepath = tmp_path / "test.h5"
    filepath = make_test_hdf5_file(_filepath)
    with h5py.File(filepath, mode="r") as f:
        groups_dict_from_file = dict(h5.groups_gen(f))

        groups_dict_from_filepath = dict(h5.groups_gen(filepath))
        assert groups_dict_from_filepath is not None
        assert sorted(groups_dict_from_filepath.keys()) == EXPECTED_GROUPS_KEYS
        assert sorted(groups_dict_from_filepath.keys()) == sorted(
            groups_dict_from_file.keys()
        )


def test_no_repeated_keys(tmp_path: Path) -> None:
    filepath = tmp_path / "test.h5"
    make_test_hdf5_file(filepath)
    with h5py.File(filepath, mode="r") as f:
        keys = set()
        for k in h5.h5py_obj_keys_gen(f):
            if k in keys:
                raise ValueError(f"Repeated key {k}")
            else:
                keys.add(k)
