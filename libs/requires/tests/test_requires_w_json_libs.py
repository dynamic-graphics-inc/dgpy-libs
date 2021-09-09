import pytest


def test_requires_json_n_rapid_json() -> None:
    from requires import requires

    @requires('json')
    def uno():
        return json.dumps({'a': 1, 'b': 2})

    @requires(
        _import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson'
    )
    def tres():
        return rapidjson.dumps({'a': 1, 'b': 2})

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e

    # with pytest.raises(ModuleNotFoundError):
    #     tres()  # Will err if not install with where to install instructions


def test_requires_json_n_rapid_json_pkg_callable() -> None:
    import requires

    @requires('json')
    def uno():
        return json.dumps({'a': 1, 'b': 2})

    @requires(
        _import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson'
    )
    def tres():
        return rapidjson.dumps({'a': 1, 'b': 2})

    try:
        tres()
    except ModuleNotFoundError as e:
        with pytest.raises(ModuleNotFoundError):
            raise e
    # with pytest.raises(ModuleNotFoundError):
    #     tres()  # Will err if not install with where to install instructions
