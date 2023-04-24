def test_shed_expoerts():
    import requires.shed as requires_shed

    assert requires_shed.__all__ == tuple(sorted(set(requires_shed.__all__)))
    shed_requirements = [el for el in dir(requires_shed) if el.startswith("requires_")]
    for shed_requirement in shed_requirements:
        assert shed_requirement in requires_shed.__all__
