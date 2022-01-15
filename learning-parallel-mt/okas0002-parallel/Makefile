#.DEFAULT_GOAL := help

HOST := 10.64.16.196
USER := okas0002

SM := 35

SOURCE_FILES := sha512.cu programme.cu
COMPILATION_CMD = nvcc -arch=sm_$(SM) $(SOURCE_FILES)
SOURCES := $(SOURCE_FILES) constants.hpp sha512.hpp jbutil.h gpu.hpp
REMOTE := $(USER)@$(HOST)


# Porcelain
# ###############
.PHONY: run run-watch build build-debug test

run: prod.out ## run the app
	./prod.out

run-debug: debug.out
	./debug.out

run-watch: ## run the app in watch mode
	ls $(SOURCES) programme.cu | entr -c make run

build: setup prod.out ## create artifact

build-debug: setup debug.out

remote:  ## sync, compile and run remotely
	rsync -aPz $(SOURCES) $(REMOTE):~/a2/
	ssh $(REMOTE) 'cd a2; $(COMPILATION_CMD) -O3 && ./a.out'


# Plumbing
# ###############
.PHONY: setup

prod.out: $(SOURCES)
	$(COMPILATION_CMD) -O3 -o prod.out

debug.out: $(SOURCES)
	$(COMPILATION_CMD) -G -g -o debug.out

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
