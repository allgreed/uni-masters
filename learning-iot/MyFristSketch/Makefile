.PHONY: build serial

build: MyFristSketch.ino
	arduino-cli compile --fqbn arduino:avr:uno $<
	touch build

build/arduino.avr.uno/..hex:
	ln -s MyFristSketch.ino.hex $@

build/arduino.avr.uno/..ino.hex:
	ln -s MyFristSketch.ino.hex $@

flash: build build/arduino.avr.uno/..hex build/arduino.avr.uno/..ino.hex
	arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno MyFirstSketch

serial:
	minicom -D /dev/ttyUSB0 -b 115200
