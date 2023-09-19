SHELL = /bin/bash
.PHONY: setup
.PHONY: docs
.PHONY: test

setup:
	pipenv install --dev

docs:
	pipenv run pdoc nrclex -d numpy -o docs/ --math --mermaid --search

test:
	pipenv lock
	pipenv requirements --dev > requirements.txt
	pipenv run tox
