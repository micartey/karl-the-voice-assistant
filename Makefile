# Makefile
SHELL := /bin/bash

PROJECT_PATH=$(shell pwd)

all: start

requirements:
	@echo "Generate requirements.txt"
	@source venv/bin/activate; ./generate_requirements.sh

install: setup
	@echo "Setup virtual environment"
	@python -m venv venv
	@source venv/bin/activate; pip install -r requirements.txt

setup:
	@if [ ! -f .env ]; then \
		cp assets/templates/.env.template .env; \
	fi

start:
	@echo "Starting voice assistant"
	@source venv/bin/activate; python -m src.main

clean:
	@echo "Clean virtual environment and requirements"
	@rm -f requirements.txt
	@rm -rf venv

service:
	@echo "Install karl as a service (Linux only)"
	sed 's|PLACEHOLDER|$(PROJECT_PATH)|' assets/templates/karl.service.ini > /etc/systemd/system/karl.service
	systemctl daemon-reload
	systemctl enable karl.service
	systemctl start karl.service