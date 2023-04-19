from shellfish import env


def test_env():
    assert "SHELLFISH_TEST" not in env
    env.SHELLFISH_TEST = "value"
    assert env.SHELLFISH_TEST == "value"
    assert env.get("SHELLFISH_TEST") == "value"
    assert env["SHELLFISH_TEST"] == "value"
