import numpy as np


def scrambler(data):
    lfsr = np.ones(7, dtype=int)
    scrambled_bits = np.zeros(len(data), dtype=int)

    for i in range(len(data)):
        val = lfsr[3] ^ lfsr[6]
        scrambled_bits[i] = data[i] ^ val
        lfsr = np.concatenate(([val], lfsr[:-1]))

    return scrambled_bits
