import numpy as np


def ofdm_mod(input_data):
    positions = [-27, -7, -4, 7, 21]
    positions_values = [1, 1, 0, 1, -1]

    num_subcarriers = len(input_data) // 52
    subcarriers = np.split(input_data, num_subcarriers)

    for i in range(len(subcarriers)):
        subcarriers[i] = np.concatenate((np.zeros(3), subcarriers[i]))
        subcarriers[i] = np.concatenate((subcarriers[i], np.zeros(4)))

        for index in range(len(positions)):
            subcarriers[i] = np.insert(subcarriers[i], positions[index] + 35, positions_values[index], axis=0)
        subcarriers[i] = np.fft.ifft(subcarriers[i])

    return subcarriers
