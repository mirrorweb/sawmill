.PHONY: env run test lint docs requirements
.DEFAULT: env

SHELL := /bin/bash

# List and check for commands.
COMMANDS = make
COMMAND_CHECK := $(foreach exec,$(COMMANDS), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

env:
	@echo "Building the python environment..."
	@poetry install

run:
	@echo "Sawmill is a library and has nothing to run!"

test:
	@source .env && poetry run coverage run --branch -m unittest discover --pattern=tests/*.py; poetry run coverage html

lint:
	@poetry run isort --virtual-env .venv **/*.py && poetry run flake8

docs:
	@poetry run sphinx-apidoc -o docs/source ./ ./tests/*.py
	@cd docs && make html

## Generate a fresh requirements.txt file from poetry environment
requirements:
	@poetry export \
	--format requirements.txt \
	--output requirements.txt \
	--without-hashes
	@poetry show --tree > poetry-show-tree
