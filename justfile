default: fmt ruff

black:
    black .

rsort:
    ruff --select "I" --show-fixes --fix .

isort:
    isort --sp pyproject.toml libs

fmt: isort black

ruff:
    ruff .

lint: fmt
    nox -s lint
