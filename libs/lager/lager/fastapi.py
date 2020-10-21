# -*- coding: utf-8 -*-
"""FastAPI logging"""
from lager.logging import intercept


FASTAPI_LOGGERS = [
    'gunicorn',
    'gunicorn.errors' 'uvicorn',
    'uvicorn.error',
    'fastapi',
    'sqlalchemy',
]


def fastapi_intercept() -> None:
    intercept(FASTAPI_LOGGERS)
