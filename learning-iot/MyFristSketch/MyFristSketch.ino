void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.write("Led is shining\n");
    delay(2000);
    digitalWrite(LED_BUILTIN, LOW);
    Serial.write("And it's gone :c\n");
    delay(2000);
}
