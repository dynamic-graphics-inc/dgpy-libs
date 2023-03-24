import time

from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import pytest

from fmts import long_timestamp_string, timestamp


def test_timestamp_float_input_local():
    utc_offset = -int(time.timezone / 3600)
    timestamp_local = datetime.fromtimestamp(
        1551111111.111111, tz=timezone(timedelta(hours=utc_offset))
    ).strftime("%Y%m%d-%H%M%S")
    assert timestamp(1551111111.111111) == timestamp_local


def test_timestamp_float_input_eastcoast():
    assert timestamp(1551111111.111111, -5) == "20190225-111151"


def test_timestamp_float_input_westcoast():
    assert timestamp(1551111111.111111, -8) == "20190225-081151"


def test_timestamp_datetime_input():
    now = datetime.now()
    assert timestamp(now) == now.strftime("%Y%m%d-%H%M%S")


def test_timestamp_no_input():
    assert timestamp() == datetime.now().strftime("%Y%m%d-%H%M%S")


def test_long_timestamp_string_westcoast():
    assert (
        long_timestamp_string(1551111111.111111, utc_offset=-8)
        == "Monday, 25. February 2019 08:11AM"
    )


def test_long_timestamp_string_local():
    utc_offset = -int(time.timezone / 3600)
    local_long_timestamp = datetime.fromtimestamp(
        1551111111.111111, tz=timezone(timedelta(hours=utc_offset))
    ).strftime("%A, %d. %B %Y %I:%M%p")
    assert long_timestamp_string(1551111111.111111) == local_long_timestamp
