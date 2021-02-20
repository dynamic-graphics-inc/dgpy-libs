.DEFAULT_GOAL := all

PKG_NAME := $(shell cat pyproject.toml | grep name | awk '{print $$3}' | sed 's/"//g')
PWD_DIRPATH = .
TESTS_DIRPATH = ${PWD}/tests

isort = isort --sp ../../pyproject.toml h5 tests
black = black -S --config ../../pyproject.toml -l 88 h5 tests

nbs = $(wildcard *.ipynb)
mds = $(nbs:%.ipynb=%.md)
pys = $(wildcard *.py)

#
all: install
.PHONY: fmt flake mypy test testcov testlf doctest clean

.PHONY: install
install:
	### MIGHT HAVE TO INSTALL POETRY
	# pip install poetry
	### NO CREATE ENV
	#python -m poetry config virtualenvs.create false
	python -m poetry install


###########################################
### LINTING, FORMATTING & TYPE CHECKING ###
###########################################
## FORMATTING
.PHONY: fmt
fmt:
	@echo $(PKG_NAME)
	$(isort)
	$(black)

## LINTING
.PHONY: flake
flake: fmt
	python -m flake8 --config=./.flake8 $(PKG_NAME)
	python -m flake8 --config=./.flake8 tests

## TYPE CHECKING
.PHONY: mypy
mypy:
	mypy --config-file ../../mypy.ini $(PKG_NAME)

###############
### TESTING ###
###############
.PHONY:test
test:
	pytest --doctest-modules tests $(PKG_NAME)

.PHONY:testcov
testcov:
	pytest --cov=dgpy_pkg --doctest-modules tests $(PKG_NAME)

.PHONY:testlf
testlf:
	pytest --doctest-modules --lf tests $(PKG_NAME)

.PHONY:doctest
doctest:
	pytest --doctest-modules $(PKG_NAME)

.PHONY:doctestcov
doctestcov:
	pytest --cov=src/dgpy --doctest-modules $(PKG_NAME)

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
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	# python setup.py clean
	rm -rf site
	#rm -rf docs/_build
	rm -rf .nox
	rm -rf .nox_*

#############
### BUILD ###
#############
.PHONY:requirements
reqs:
	@poetry export --without-hashes -o requirements.txt -f requirements.txt
	@poetry export --without-hashes --dev -o requirements-dev.txt -f requirements.txt

.PHONY: build
build:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf *.egg-info
	rm -rfv dist.bak || true
	mv dist dist.bak || true
	python -m poetry build -f wheel
	mv -f dist.bak/* dist
	rm -rfv dist.bak || true
