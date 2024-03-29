default: fmt ruff

black:
    black .

rsort:
    ruff --select "I" --show-fixes --fix .

isort:
    isort --sp pyproject.toml libs

codespell:
    codespell .

fmt: black

ruff:
    ruff check .

ruffmt:
    ruff format .

noxlint:
    nox -s lint

lint: fmt noxlint codespell
