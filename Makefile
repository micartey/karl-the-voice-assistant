# Makefile
SHELL := /bin/bash

all: start

requirements:
	@echo "Generate requirements.txt"
	@source venv/bin/activate; ./generate_requirements.sh

install:
	@echo "Setup virtual environment"
	@python -m venv venv
	@source venv/bin/activate; pip install -r requirements.txt

setup: install
	@rm -rf .env
	@cp assets/templates/.env.template .env

start:
	@echo "Starting voice assistant"
	@source venv/bin/activate; python -m src.main

clean:
	@echo "Clean virtual environment and requirements"
	@rm -f requirements.txt
	@rm -rf venv
