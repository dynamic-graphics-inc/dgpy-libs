#!/usr/bin/env just --justfile
# 'justfile'
# just-repo: https://github.com/casey/just
# just-docs: https://just.systems/man/en/
# list all targets (default)
@_default:
    just --list --unsorted

dev:
    uv sync --all-extras --dev

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
fmt-pyproject:
    find . -type f -name pyproject.toml | xargs -n1 pyproject-fmt

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
    nox -s mypy

# lint
lint: fmt noxlint

# format the justfile(s) (w/ just)
fmt-justfile:
    just --fmt --unstable

# nuke poetry cache
poetry-nuke-cache:
    poetry cache clear pypi --all -v
