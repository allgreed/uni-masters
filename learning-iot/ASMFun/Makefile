.PHONY: build serial
PROJECT := ASMFun

build: $(PROJECT).ino
	arduino-cli compile --fqbn arduino:avr:uno $<
	touch build

build/arduino.avr.uno/..hex:
	ln -s $(PROJECT).ino.hex $@

build/arduino.avr.uno/..ino.hex:
	ln -s $(PROJECT).ino.hex $@

flash: build build/arduino.avr.uno/..hex build/arduino.avr.uno/..ino.hex
	arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno $(PROJECT)

serial:
	minicom -D /dev/ttyUSB0 -b 115200
