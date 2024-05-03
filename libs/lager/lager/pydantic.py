# -*- coding: utf-8 -*-
"""Lager & pydantic"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

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
    type: Optional[Type[BaseException]]
    value: Optional[BaseException]
    traceback: Optional[TracebackType]


class Record(JsonBaseModel):
    elapsed: timedelta
    exception: Optional[RecordException]
    extra: Dict[Any, Any]
    file: RecordFile
    function: str
    level: RecordLevel
    line: int
    message: str
    module: str
    name: Union[str, None]
    process: RecordProcess
    thread: RecordThread
    time: datetime


class Message(JsonBaseModel):
    record: Record
