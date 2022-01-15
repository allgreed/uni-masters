.PHONY: flash

CPU_FREQUENCY := 16000000
BAUD := 115200

main.bin: main.c
	avr-gcc -Wall -g -Os -mmcu=atmega328p -o main.bin main.c

main.hex: main.bin
	avr-objcopy -j .text -j .data -O ihex main.bin main.hex

flash: main.hex
	avrdude -p atmega328p -carduino -U flash:w:main.hex:i -F -P /dev/ttyUSB0

serial:
	minicom -D /dev/ttyUSB0 -b $(BAUD)
