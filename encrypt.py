WORD_SIZE = 32
MASK32 = (1 << WORD_SIZE) - 1


def rotl(x, r):
    return ((x << r) | (x >> (32 - r))) & MASK32


def rotr(x, r):
    return ((x >> r) | (x << (32 - r))) & MASK32


def sbox(x):
    x ^= 0x3C3C3C3C
    x = rotl(x, 5)
    x ^= 0xA5A5A5A5
    return x & MASK32


PBOX = [
    0, 8, 16, 24,
    1, 9, 17, 25,
    2, 10, 18, 26,
    3, 11, 19, 27,
    4, 12, 20, 28,
    5, 13, 21, 29,
    6, 14, 22, 30,
    7, 15, 23, 31
]


def pbox(x):
    y = 0
    for i, j in enumerate(PBOX):
        y |= ((x >> i) & 1) << j
    return y & MASK32


def round_func(x, k, rc):
    x ^= k
    x ^= rc
    x = sbox(x)
    x = pbox(x)
    return x & MASK32


def derive_t(ka, kb):
    ka = sbox(rotl(ka, 3))
    kb = sbox(rotr(kb, 7))

    rc1 = 0x11111111
    rc2 = 0x22222222

    t1 = round_func(ka, ka, rc1)
    t2 = round_func(kb, kb, rc2)

    return t1, t2



def encrypt_message(message_bytes, keyA, keyB):
    message = int.from_bytes(message_bytes, "big")   
    t1, t2 = derive_t(keyA, keyB)

    c1 = message ^ t1
    c2 = c1 ^ t2
    c3 = c2 ^ t1

    return c1, c2, c3

    

if __name__ == "__main__":
    # C1,C2,C3=encrypt_message(Flag,KeyA,KeyB) : This is how the first function is called.
    
