import numpy as np


def check_r(input_r):
    if input_r == "1/2":
        return np.array([[1], [1]], dtype=int)
    elif input_r == "2/3":
        return np.array([[1, 1], [1, 0]], dtype=int)
    elif input_r == "3/4":
        return np.array([[1, 1, 0], [1, 0, 1]], dtype=int)
    elif input_r == "4/5":
        return np.array([[1, 1, 1, 1], [1, 0, 0, 0]], dtype=int)
    elif input_r == "5/6":
        return np.array([[1, 1, 0, 1, 0], [1, 0, 1, 0, 1]], dtype=int)
    else:
        return False


def bcc_fec(data, input_r):
    genpol1 = np.array([1, 0, 1, 1, 0, 1, 1], dtype=int)
    genpol2 = np.array([1, 1, 1, 1, 0, 0, 1], dtype=int)

    state = np.zeros(7, dtype=int)
    bcc_encoded_data = np.zeros((2, len(data)), dtype=int)

    for i in range(len(data)):
        state = np.concatenate(([data[i]], state[:-1]))

        output_dataA = np.mod(np.sum(state * genpol1), 2)
        output_dataB = np.mod(np.sum(state * genpol2), 2)

        bcc_encoded_data[0, i] = output_dataA
        bcc_encoded_data[1, i] = output_dataB

    puncturing_template = check_r(input_r)

    rows, cols = bcc_encoded_data.shape
    puncturing_rows, puncturing_cols = puncturing_template.shape

    punctured_data = np.zeros_like(bcc_encoded_data)

    for i in range(rows):
        for j in range(cols):
            puncturing_row = i % puncturing_rows
            puncturing_col = j % puncturing_cols
            punctured_data[i, j] = bcc_encoded_data[i, j] * puncturing_template[puncturing_row, puncturing_col]

    return punctured_data
