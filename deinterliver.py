import numpy as np


def deinterleaver(interleaved_vector):
    rows = 2
    cols = int(len(interleaved_vector) / 2)

    interleaved_matrix = interleaved_vector.reshape((cols, rows))

    original_matrix = np.zeros((rows, cols), dtype=int)

    for j in range(cols):
        for i in range(rows):
            original_matrix[i][j] = interleaved_matrix[j][i]

    return original_matrix
