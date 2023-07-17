.DEFAULT_GOAL := all

LIBS := $(shell ls libs)
PWD_DIRPATH = .

isort = isort --sp pyproject.toml libs
black = black --config pyproject.toml libs

nbs = $(wildcard *.ipynb)
mds = $(nbs:%.ipynb=%.md)
pys = $(wildcard *.py)

.PHONY: fmt
fmt:
	isort --sp pyproject.toml libs dgpydev tests .
	black --config pyproject.toml libs dgpydev tests .

.PHONY: flake
flake: fmt
	python -m flake8 --config=./.flake8 libs

.PHONY: isort_check
isort_check:
	isort --sp pyproject.toml libs --check

.PHONY: lint
lint:
	black --config pyproject.toml libs --check

.PHONY: mypy
mypy:
	mypy --version
	mypy --config-file pyproject.toml libs

.PHONY: nukepoetry
nukepoetry:
	poetry cache clear pypi --all -v

.PHONY: ruff
ruff:
	ruff .

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
