.global addasm
addasm:
    toret_l = 24    
    toret_h = 25
    add toret_l, r22
    adc toret_h, r23
    ret
