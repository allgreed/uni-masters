PROJECT := assignment2

# Porcelain
# ###############
.PHONY: run flash build test serial

run: setup ## run the app
	python main.py

test: setup ## run unit tests
	pytest

flash: build setup ## upload the programme to microcontroller
	arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno $(PROJECT)

build: $(PROJECT).ino build/arduino.avr.uno/..ino.hex setup ## build IoT payload
	arduino-cli compile --fqbn arduino:avr:uno $<
	touch build

serial:
	minicom -D /dev/ttyUSB0 -b 9600

# Plumbing
# ###############
.PHONY: setup

build/arduino.avr.uno/..hex:
	ln -s $(PROJECT).ino.hex $@

build/arduino.avr.uno/..ino.hex:
	ln -s $(PROJECT).ino.hex $@

haarcascade_frontalface_default.xml:
	@echo Accepting EULA!
	wget https://raw.githubusercontent.com/shantnu/Webcam-Face-Detect/master/haarcascade_frontalface_default.xml

setup: haarcascade_frontalface_default.xml

# Helpers
# ###############
.PHONY: install-low-power

install-low-power: ## install Low-Power library
	arduino-cli lib install Low-Power

# Utilities
# ###############
.PHONY: help todo clean really_clean init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: ## remove artifacts

really_clean: ## remove EVERYTHING

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help
