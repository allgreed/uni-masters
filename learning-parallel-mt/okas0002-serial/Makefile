#.DEFAULT_GOAL := help

COMPILATION_CMD = g++ -lstdc++ -lm -o $@ sha512.cpp 
SOURCES := sha512.cpp constants.hpp sha512.hpp

# Porcelain
# ###############
.PHONY: run run-watch build build-debug test

run: prod.out ## run the app
	./prod.out

run-debug: debug.out
	./debug.out

run-watch: ## run the app in watch mode
	ls $(SOURCES) programme.cpp | entr -c make run

build: setup  ## create artifact

build-debug: setup debug.out

test: test.out
	./test.out

# Plumbing
# ###############
.PHONY: setup

test.out: $(SOURCES) test.cpp
	$(COMPILATION_CMD) test.cpp -g

prod.out: $(SOURCES) programme.cpp
	$(COMPILATION_CMD) programme.cpp -O3 -Wall

debug.out: $(SOURCES) programme.cpp
	$(COMPILATION_CMD) programme.cpp -g -Wall

setup:


# Utilities
# ###############
.PHONY: help todo init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
