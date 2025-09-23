from shellfish.done import HrTime


def test_hrtime_legacy_aliases() -> None:
    """Test that HrTime works with legacy aliases."""
    d = HrTime.model_validate({"sec": 12, "ns": 34}).model_dump()

    assert d == {"secs": 12, "nanos": 34}
    assert d == HrTime.model_validate({"secs": 12, "nanos": 34}).model_dump()
