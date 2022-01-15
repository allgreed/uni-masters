#include <stdlib.h>

extern "C" {
    uint16_t addasm(uint16_t ia, uint16_t ib);
}

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.write("Led is shining\n");
    delay(1000);

    char str[10];
    /*uint16_t retval = addasm(0x0102, 0x0203); */
    uint16_t retval = addasm(0x01ff, 0x0201); 
    itoa(retval, str, 16);

    digitalWrite(LED_BUILTIN, LOW);
    Serial.write(str);
    delay(1000);
}
