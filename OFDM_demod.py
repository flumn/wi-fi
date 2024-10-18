import numpy as np


def ofdm_demod(subcarriers):
    positions = [21, 7, -4, -7, -27]
    demoduldated_data = []

    for subcarrier in subcarriers:
        subcarrier = np.fft.fft(subcarrier)

        for index in range(len(positions)):
            subcarrier = np.delete(subcarrier, positions[index] + 35)

        subcarrier = subcarrier[3:-4]
        demoduldated_data.append(np.round(subcarrier, 0))

    demoduldated_data = np.concatenate(demoduldated_data)

    return demoduldated_data
