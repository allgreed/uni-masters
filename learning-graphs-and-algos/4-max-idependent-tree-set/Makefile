
# Porcelain
# ###############
.PHONY: run watch
 
run:
	python main.py

watch:
	ls main.py | entr -c make --no-print-directory run

test:
	pytest

test-watch:
	ls main.py test_main.py | entr -c make --no-print-directory test

# Plumbing
# ###############
.PHONY: gitclean gitclean-with-libs

gitclean:
	@# will remove everything in .gitignore expect for blocks starting with dep* or lib* comment

	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' .gitignore | grep '\S' | sort) <(awk '/^# *(dep|lib)/,/^$/' testowy | head -n -1 | tail -n +2 | sort) | xargs rm -rf

gitclean-with-libs:
	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' .gitignore | grep '\S' | sort) | xargs rm -rf


# Utilities
# ###############
.PHONY: help todo clean really_clean
todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: gitclean ## remove artifacts

really_clean: gitclean-with-libs ## remove EVERYTHING

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help
