def test_funkify_module():
    from tests import a_module

    assert a_module.main() == 123
    assert a_module() == 123
