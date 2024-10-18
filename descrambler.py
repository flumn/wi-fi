import numpy as np


def descrambler(data):
    lfsr = np.ones(7, dtype=int)
    descrambled_bits = np.zeros(len(data), dtype=int)

    for i in range(len(data)):
        val = lfsr[3] ^ lfsr[6]
        descrambled_bits[i] = data[i] ^ val
        lfsr = np.concatenate(([val], lfsr[:-1]))

    return descrambled_bits
