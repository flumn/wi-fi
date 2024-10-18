import numpy as np
from constellation_dicts import *


def constellation_mapper(input_bits, mode):
    manipulation_array = np.array([], dtype=complex)

    if mode == "bpsk":
        for i in range(0, len(input_bits)):
            key = input_bits[i]
            positions = bpsk_map_dict[key]
            manipulation_array = np.append(manipulation_array, positions)
    elif mode == "qpsk":
        for i in range(0, len(input_bits) - 1, 2):
            key = tuple(input_bits[i:i + 2])
            positions = qpsk_map_dict[key]
            manipulation_array = np.append(manipulation_array, positions)
    elif mode == "qam16":
        for i in range(0, len(input_bits) - 3, 4):
            key = tuple(input_bits[i:i + 4])
            positions = qam16_map_dict[key]
            manipulation_array = np.append(manipulation_array, positions)
    elif mode == "qam64":
        for i in range(0, len(input_bits) - 5, 6):
            key = tuple(input_bits[i:i + 6])
            positions = qam64_map_dict[key]
            manipulation_array = np.append(manipulation_array, positions)

    return manipulation_array
