# -*- coding: utf-8 -*-
"""Lager & pydantic"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from jsonbourne.pydantic import JsonBaseModel

if TYPE_CHECKING:
    from datetime import datetime, timedelta
    from types import TracebackType


class RecordFile(JsonBaseModel):
    name: str
    path: str


class RecordLevel(JsonBaseModel):
    name: str
    no: int
    icon: str


class RecordThread(JsonBaseModel):
    id: int
    name: str


class RecordProcess(JsonBaseModel):
    id: int
    name: str


class RecordException(JsonBaseModel):
    type: type[BaseException] | None
    value: BaseException | None
    traceback: TracebackType | None


class Record(JsonBaseModel):
    elapsed: timedelta
    exception: RecordException | None
    extra: dict[Any, Any]
    file: RecordFile
    function: str
    level: RecordLevel
    line: int
    message: str
    module: str
    name: str | None
    process: RecordProcess
    thread: RecordThread
    time: datetime


class Message(JsonBaseModel):
    record: Record
