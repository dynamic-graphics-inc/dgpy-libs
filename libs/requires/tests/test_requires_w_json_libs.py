def test_requires_json_n_rapid_json():
    from requires import requires

    @requires('json')
    def uno():
        return json.dumps({'a': 1, 'b': 2})

    uno()

    @requires(
        _import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson'
    )
    def tres():
        return rapidjson.dumps({'a': 1, 'b': 2})

    tres()  # Will err if not install with where to install instructions


def test_requires_json_n_rapid_json_pkg_callable():
    import requires

    @requires('json')
    def uno():
        return json.dumps({'a': 1, 'b': 2})

    uno()

    @requires(
        _import='rapidjson', pip='python-rapidjson', conda_forge='python-rapidjson'
    )
    def tres():
        return rapidjson.dumps({'a': 1, 'b': 2})

    tres()  # Will err if not install with where to install instructions
