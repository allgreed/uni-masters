void uart_putchar(char c)
{
    loop_until_bit_is_set(UCSR0A, UDRE0); // this is a macro, essentially a busy loop
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
