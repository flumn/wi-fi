import numpy as np


def interleaver(input_matrix):
    interleaved_matrix = np.zeros(input_matrix.shape[::-1], dtype=int)

    for j in range(input_matrix.shape[1]):
        temp = []
        for i in range(input_matrix.shape[0]):
            temp.append(int(input_matrix[i][j]))
        interleaved_matrix[j] = temp

    interleaved_vector = interleaved_matrix.reshape(1, input_matrix.shape[0] * input_matrix.shape[1])[0]

    return interleaved_vector
