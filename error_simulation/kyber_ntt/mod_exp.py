def mod_exp_lsb_lbit(base, exponent, modulus, l):
    """
    LSB-first (right-to-left) modular exponentiation
    Returns (final_result, r_mid)
    r_mid = a^(lower l/2 bits of exponent) mod m
    *base is message*
    """
    result = 1
    base %= modulus
    r_mid = None

    for i in range(l):
        # If current LSB is 1 → multiply
        if exponent & 1:
            result = (result * base) % modulus
        
        
        # Capture mid-state after l/2 bits
        if i == (l // 2 - 1):
            r_mid = result

        # Square base every cycle
        base = (base * base) % modulus
        print (f"e_flag: {exponent & 1}, rb_barret_op: {result}, bb_barret_op: {base}")
        exponent >>= 1
        
    return result, r_mid
a = 1133
e = 3223
m = 3329
l = 12

el = e %  (2 ** (l // 2))     # lower bits
eh = e // (2 ** (l // 2))     # upper bits

final, r_mid = mod_exp_lsb_lbit(a, e, m, l)

r1 = pow(a, el, m)
r2 = pow(a, eh * (2 ** (l // 2)), m)

print("final result:", final)
print("r_mid :", r_mid)
print("r1    :", r1)
print("r2    :", r2)
print("check :", (r_mid * r2) % m)
