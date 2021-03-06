.DEFAULT_GOAL := all

LIBS := $(shell ls libs)
PWD_DIRPATH = .

isort = isort --sp pyproject.toml libs
black = black -S --config pyproject.toml -l 88 libs

nbs = $(wildcard *.ipynb)
mds = $(nbs:%.ipynb=%.md)
pys = $(wildcard *.py)

## FORMATTING
.PHONY: fmt
fmt:
	echo $(LIBS)
	$(isort)
	$(black)

## LINTING
.PHONY: flake
flake: fmt
	python -m flake8 --config=./.flake8 --verbose $(PKG_NAME)

###########
## CLEAN ##
###########
.PHONY: clean
clean:
	rm -rfv dist || true
	rm -rfv build || true
	# rm -rfv docs/docs_sphinx/_build/ || true
	rm -rfv site || true
	#
	rm -rfv `find . -name __pycache__`
	rm -fv `find . -type f -name '*.py[co]' `
	rm -fv `find . -type f -name '*~' `
	rm -fv `find . -type f -name '.*~' `
	rm -rfv .cache
	rm -rfv .pytest_cache
	rm -rfv .mypy_cache
	rm -rfv htmlcov
	rm -rfv *.egg-info
	rm -fv .coverage
	rm -fv .coverage.*
	rm -rfv build
	rm -rfv dist
	# python setup.py clean
	rm -rfv site
	#rm -rf docs/_build
	rm -rfv .nox
	rm -rfv .nox_*
