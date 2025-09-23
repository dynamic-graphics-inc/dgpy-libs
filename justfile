#!/usr/bin/env just --justfile
# 'justfile'
# just-repo: https://github.com/casey/just
# just-docs: https://just.systems/man/en/
# list all targets (default)
@_default:
    just --list --unsorted

# sync && test
dev: test

# sync deps
sync:
    uv sync --all-extras --dev

# build packages
build:
    rm -rfv dist
    uv build -v --package aiopen
    uv build -v --package asyncify
    uv build -v --package fmts
    uv build -v --package funkify
    uv build -v --package h5
    uv build -v --package jsonbourne
    uv build -v --package lager
    uv build -v --package listless
    uv build -v --package requires
    uv build -v --package shellfish
    uv build -v --package xtyping

# test root + all libraries
test: sync
    uv run pytest tests dgpydev
    cd libs/aiopen && uv run pytest
    cd libs/asyncify && uv run pytest
    cd libs/dgpylibs && uv run pytest
    cd libs/dgpytest && uv run pytest
    cd libs/fmts && uv run pytest
    cd libs/funkify && uv run pytest
    cd libs/h5 && uv run pytest
    cd libs/jsonbourne && uv run pytest
    cd libs/lager && uv run pytest
    cd libs/listless && uv run pytest
    cd libs/requires && uv run pytest
    cd libs/shellfish && uv run pytest
    cd libs/xtyping && uv run pytest

# test a specific library `just test-lib h5`
test-lib dgpylib: dev
    cd libs/{{dgpylib}} && uv run pytest

# test all libraries
test-all: (test-lib "aiopen") (test-lib "asyncify") (test-lib "dgpylibs") (test-lib "dgpytest") (test-lib "fmts") (test-lib "funkify") (test-lib "h5") (test-lib "jsonbourne") (test-lib "lager") (test-lib "listless") (test-lib "requires") (test-lib "shellfish") (test-lib "xtyping")

# fix imports
rsort:
    ruff check --select "I" --show-fixes --fix .

# sort imports
isort: rsort

# check spelling
codespell:
    codespell .

# format python
fmt:
    ruff format
    ruff check --select "I,RUF022" --show-fixes --fix --unsafe-fixes .

# fmt pyproject.toml files
pyproject-fmt:
    find . -type f -name pyproject.toml | xargs -n1 pyproject-fmt --keep-full-version

# format-check
fmtc:
    ruff format --check
    ruff check --select "I" --show-fixes .

# ruff lint
ruff:
    ruff check .

# ruff lint & fix
ruffix:
    ruff check . --fix

# nox lint
noxlint:
    nox -s lint

# mypy
mypy: fmt
    uv run nox -s mypy

# lint
lint: fmt noxlint

# format the justfile(s) (w/ just)
fmt-justfile:
    just --fmt --unstable
