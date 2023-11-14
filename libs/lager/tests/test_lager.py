# -*- coding: utf-8 -*-
"""
test_lager
----------------------------------

Tests for `lager` module.
"""


from __future__ import annotations


def test_lager_port() -> None:
    from lager import const

    assert const.LAGER_PORT == 52437
