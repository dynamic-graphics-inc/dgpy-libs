default: fmt ruff

black:
    black .

isort:
    ruff --select "I" --show-fixes --fix .

fmt: isort black

ruff:
    ruff .

