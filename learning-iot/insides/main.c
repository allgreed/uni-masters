// TODO: move this into the makefile
#define F_CPU 16000000UL
#define BAUD 115200

#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/sleep.h>
#include <util/setbaud.h>

#include <string.h>

#define LED_PIN PB5
// TODO: can this be done more sensibly?
// TODO: question: why using this particular prescaler?
#define TIMER_PRESCALER CS12 // 256
#define TIMER_PRESCALER_RATE 256
#define TICKS_PER_SECOND(prescaler_rate) (F_CPU / prescaler_rate)

char * MSG = "interrupted!";

void uart_putchar(char c)
{
    loop_until_bit_is_set(UCSR0A, UDRE0);
    UDR0 = c;
}

void uart_println(char * s)
{
    for(int i = 0; i < strlen(s); ++i)
    {
        uart_putchar(s[i]);
    }
    uart_putchar('\n');
}

ISR(TIMER1_COMPA_vect)
{
    uart_println(MSG);
    PORTB ^= _BV(LED_PIN);
}

int main() 
{
    DDRB |= _BV(LED_PIN);
    TCCR1B |= _BV(TIMER_PRESCALER) + _BV(WGM12); // WGM12 is clearing the timer on compare
    TIMSK1 = _BV(OCIE1A);
    OCR1A = TICKS_PER_SECOND(TIMER_PRESCALER_RATE);

    UBRR0H = UBRRH_VALUE;
    UBRR0L = UBRRL_VALUE;
#if USE_2X
    UCSR0A |= _BV(U2X0);
#else
    UCSR0A &= ~(_BV(U2X0));
#endif
    UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
    UCSR0B = _BV(RXEN0) | _BV(TXEN0);

    set_sleep_mode (SLEEP_MODE_IDLE);  
    sleep_enable();
    sei();
    sleep_cpu(); 
    sleep_disable();
    MSG = "huh?";
    while (1)
    {

    }
} 
