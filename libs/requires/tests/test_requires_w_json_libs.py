import pytest


def test_requires_json_n_rapid_json() -> None:
    from requires import requires

    @requires("json")
    def uno():
        return json.dumps({"a": 1, "b": 2})

    @requires(
        _import="rapidjson",
        pip="python-rapidjson",
        conda_forge="python-rapidjson",
    )
    def tres():
        return rapidjson.dumps({"a": 1, "b": 2})

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e


def test_requires_json_n_rapid_json_pkg_callable() -> None:
    import requires

    @requires("json")
    def uno() -> str:
        return json.dumps({"a": 1, "b": 2})

    @requires(
        _import="rapidjson",
        pip="python-rapidjson",
        conda_forge="python-rapidjson",
    )
    def tres() -> str:
        return rapidjson.dumps({"a": 1, "b": 2})

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e
