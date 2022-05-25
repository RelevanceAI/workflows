.PHONY: all install update test clean lint
#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = python3
TEST_PATH ?= .
ENVIRONMENT ?= sandbox## sandbox/development/production
AWS_PROFILE ?= relevance-sandbox.AdministratorAccess

#################################################################################
# COMMANDS                                                                      #
#################################################################################
all:
	echo $(AWS_PROFILE)

## Install dependencies
install:
	python -m venv .venv
	. .venv/bin/activate
	pip install --upgrade pip
	pip install -q -r requirements-dev.txt
	pre-commit install

## Update dependencies
update:
	pip install -U -q -r requirements-dev.txt

update-db:
	python scripts/manual_add_to_db.py

## Upload notebooks to S3 and update ds
upload:
	aws s3 cp workflows s3://relevance-development-ap-southeast-2-workflows/$(ENVIRONMENT)/ --recursive
	aws s3 cp workflows s3://relevance-development-us-east-1-workflows/$(ENVIRONMENT)/ --recursive

## Test dependencies
test:
	python scripts/test_notebooks.py

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type f -name "*.log[s]" -delete
	find . -type f -name "*.temp" -delete
	find . -type d -name "*.coverage" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.coverage" -exec rm -rf {} +
	find . -type d -name "*.eggs" -exec rm -rf {} +
	find . -type d -name "*.pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.ipynb_checkpoints" -exec rm -rf {} +
	find . -type d -empty -delete


## Lint using flake8
lint:
	flake8 relevanceai


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
