.DEFAULT_GOAL := help

TYPE ?= single
THREADS ?= 2
TYPE_CAPITALIZED = $(shell echo '$(TYPE)' | tr '[:lower:]' '[:upper:]')
COMPILATION_CMD = gcc programme.cpp -lstdc++ -lm -lpthread -o $@ -O3 -DP_$(TYPE_CAPITALIZED) -DTHREADS=$(THREADS)

# Porcelain
# ###############
.PHONY: run run-watch build lint test

run: build ## run the app
	./a-$(TYPE).out

run-watch: ## run the app in watch mode
	ls programme.cpp | entr -c make run

build: setup a-$(TYPE).out ## create artifact

lint: setup ## run static analysis
	@echo "Not implemented"; false

test: setup ## run all tests
	@echo "Not implemented"; false

a-$(TYPE).s: programme.cpp ## ouptut assembly
	$(COMPILATION_CMD) -S -g -masm=intel

# Plumbing
# ###############
.PHONY: setup gitclean gitclean-with-libs

a-$(TYPE).out: programme.cpp ../shared/jbutil.h
	$(COMPILATION_CMD)
	

setup:

gitclean:
	@# will remove everything in .gitignore expect for blocks starting with dep* or lib* comment
	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' .gitignore | grep '\S' | sort) <(awk '/^# *(dep|lib)/,/^$/' testowy | head -n -1 | tail -n +2 | sort) | xargs rm -rf

gitclean-with-libs:
	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' .gitignore | grep '\S' | sort) | xargs rm -rf

# Helpers
# ###############
.PHONY:

# Utilities
# ###############
.PHONY: help todo clean really_clean init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: gitclean ## remove artifacts

really_clean: gitclean-with-libs clean ## remove EVERYTHING

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
