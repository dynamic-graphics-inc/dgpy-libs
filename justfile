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
    uv build -v --package h5
    uv build -v --package jsonbourne
    uv build -v --package lager
    uv build -v --package listless
    uv build -v --package requires
    uv build -v --package shellfish

# preview which libs would publish (versions not yet on PyPI)
publish-check:
    uv run python scripts/pypi_publish_detect.py

# bump one lib's version, e.g. `just bump shellfish patch`
bump pkg level="patch":
    uv version --bump {{ level }} --package {{ pkg }}

# test root + all libraries
test: sync
    uv run pytest tests dgpydev
    cd libs/aiopen && uv run pytest
    cd libs/asyncify && uv run pytest
    cd libs/dgpylibs && uv run pytest
    cd libs/dgpytest && uv run pytest
    cd libs/fmts && uv run pytest
    cd libs/h5 && uv run pytest
    cd libs/jsonbourne && uv run pytest
    cd libs/lager && uv run pytest
    cd libs/listless && uv run pytest
    cd libs/requires && uv run pytest
    cd libs/shellfish && uv run pytest

# test a specific library `just test-lib h5`
test-lib dgpylib: sync
    cd libs/{{dgpylib}} && uv run pytest

# fix imports
rsort:
    uv run ruff check --select "I" --show-fixes --fix .

# check spelling (typos; config in pyproject.toml)
typos *ARGS:
    typos {{ ARGS }}

# format python
fmt:
    uv run ruff format
    uv run ruff check --select "I,RUF022" --show-fixes --fix --unsafe-fixes .
    pnpx prettier@latest -w --prose-wrap=always CHANGELOG.md

# fmt pyproject.toml files
pyproject-fmt:
    uvx pyproject-fmt --keep-full-version pyproject.toml libs/*/pyproject.toml

# format-check
fmtc:
    uv run ruff format --check
    uv run ruff check --select "I" --show-fixes .

# ruff lint
ruff +ARGS=".":
    uv run ruff --version
    uv run ruff check {{ ARGS }}

# mypy (per-lib b/c each lib has a `tests` package)
mypy:
    #!/usr/bin/env bash
    set -euo pipefail
    uv run mypy --version
    libs=(aiopen asyncify dgpylibs dgpytest fmts h5 jsonbourne lager listless requires shellfish)
    srcs=()
    for lib in "${libs[@]}"; do srcs+=("libs/$lib/src/$lib"); done
    for lib in "${libs[@]}"; do
        echo "--- mypy: $lib"
        uv run mypy --show-error-codes --config-file pyproject.toml "${srcs[@]}" "libs/$lib/tests"
    done

# pyrefly typecheck
pyrefly *ARGS:
    uv run pyrefly --version
    uv run pyrefly check {{ ARGS }}

# ty typecheck
ty *ARGS:
    uv run ty --version
    uv run ty check {{ ARGS }}

# typecheck
typecheck: ty pyrefly mypy

# lint
lint: fmt ty pyrefly mypy

# --- docs (zensical; config in zensical.toml) ---

# serve docs w/ live reload on :8000, e.g. `just docs` or `just docs -o -a localhost:8001`
docs *ARGS:
    uv run --extra docs zensical serve {{ ARGS }}

# build docs -> public/ (same as ci)
docs-build:
    uv run --extra docs zensical build --clean

# regenerate docs/notebooks/*.md from the .ipynb files
docs-nb:
    bash scripts/mkreadnb.sh

# format the justfile(s) (w/ just)
fmt-justfile:
    just --fmt --unstable
