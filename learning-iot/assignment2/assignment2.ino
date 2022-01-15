#include <LowPower.h>

#define F_CPU 16000000UL
#define BAUD 9600
#include <util/setbaud.h>

constexpr char THE_PIN = 6;
constexpr int  DELAY_MS = 2000;
constexpr char COMMAND_OPEN = 'x';


char command = 0;

void setup() {
    pinMode(THE_PIN, OUTPUT);

    UBRR0H = UBRRH_VALUE;
    UBRR0L = UBRRL_VALUE;
    UCSR0C |= (1 << UCSZ01) | (1 << UCSZ00);
    UCSR0B |= (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);

    interrupts();
}

void loop() {
    if (command == COMMAND_OPEN)
    {
        digitalWrite(THE_PIN, HIGH);

        delay(DELAY_MS);

        command = 0;
        digitalWrite(THE_PIN, LOW);
    }

    LowPower.idle(SLEEP_FOREVER, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, SPI_OFF, USART0_ON, TWI_OFF);
}

ISR(USART_RX_vect)
{
    command=UDR0;
}
