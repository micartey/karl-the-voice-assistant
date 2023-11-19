# Makefile
SHELL := /bin/bash

# Definieren des Standardzieles
all: requirements

# Regel zum Erstellen der requirements.txt
requirements:
	@echo "Generate requirements.txt"
	@source venv/bin/activate; pip freeze > requirements.txt

install:
	@echo "Setup virtual environment"
	@python -m venv venv
	@source venv/bin/activate; pip install -r requirements.txt

setup: install
	@rm -rf .env
	@cp assets/templates/.env.template .env

start:
	@echo "Start voice assistant"
	@source venv/bin/activate; python -m src.main

clean:
	@echo "Clean virtual environment and requirements"
	@rm -f requirements.txt
	@rm -rf venv
