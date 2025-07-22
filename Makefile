all: build run

build:
	@cd backends/client-api && docker-compose build
	@cd frontends/desktop-app && make build

run: run-backend start

start:
	@cd frontends/desktop-app && make run

run-backend:
	@cd backends/client-api && docker-compose up -d

.PHONY: all build run run-backend start
