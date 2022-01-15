.global testasm
testasm:
    toret = 24
    mydta = 12
    mymem = 0x164
    factor = 0x10 # macro substiutions, essentially a #define
    rrr = 123 # this is redundant (and usless)
    ldi r19, mydta # populate r19 with the integer 12
    ori r19, factor # or with constant
    sts mymem, r19 # write contents of r19 to SRAM 0x164 address
    mov toret, r19 # returns value under register 19 [by convention the 24th register is uint_8 return]
    ret # ends function call

essentially:
    r19 <- 12
    r19 |= 16 [r19 <- 28]
    0x164 <- 28
    r24 <- 28 [return value]

28 [base 10, uint8] will be returned!
