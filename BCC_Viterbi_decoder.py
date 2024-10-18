from BCC_FEC import check_r
import numpy as np


def restore_punctured_data(punctured_data, input_r):
    rows, cols = punctured_data.shape

    puncturing_template = check_r(input_r)
    puncturing_rows, puncturing_cols = puncturing_template.shape

    restored_data = np.zeros((rows, cols), dtype=int)

    for i in range(rows):
        for j in range(cols):
            puncturing_row = i % puncturing_rows
            puncturing_col = j % puncturing_cols

            if puncturing_template[puncturing_row, puncturing_col] == 1:
                restored_data[i, j] = punctured_data[i, j]
            else:
                restored_data[i, j] = -1

    return restored_data


def calculate_branch_metric(encoded_bits, expected_output):
    metric = 0
    for i in range(len(encoded_bits)):
        if encoded_bits[i] != -1:
            metric += np.bitwise_xor(encoded_bits[i], expected_output[i])
    return metric


def bcc_decoder(encoded_bits, constraint_length):
    trellis = build_trellis(constraint_length)
    num_states = 2 ** (constraint_length - 1)
    num_bits = len(encoded_bits[0])

    path_metric = np.full((num_states, num_bits + 1), np.inf)
    path_metric[0, 0] = 0
    prev_state = np.zeros((num_states, num_bits + 1), dtype=int)

    for t in range(num_bits):
        for state in range(num_states):
            for input_bit in range(2):
                next_state = trellis[state][input_bit]['next_state']
                output = trellis[state][input_bit]['output']

                branch_metric = calculate_branch_metric(encoded_bits[:, t], output)
                new_metric = path_metric[state, t] + branch_metric

                if new_metric < path_metric[next_state, t + 1]:
                    path_metric[next_state, t + 1] = new_metric
                    prev_state[next_state, t + 1] = state

    decoded_bits = np.zeros(num_bits, dtype=int)
    state = np.argmin(path_metric[:, -1])

    for t in range(num_bits - 1, -1, -1):
        prev = prev_state[state, t + 1]
        for input_bit in range(2):
            if trellis[prev][input_bit]['next_state'] == state:
                decoded_bits[t] = input_bit
                break
        state = prev

    return decoded_bits


def build_trellis(constraint_length):
    g1 = np.array([1, 0, 1, 1, 0, 1, 1])
    g2 = np.array([1, 1, 1, 1, 0, 0, 1])
    num_states = 2 ** (constraint_length - 1)
    trellis = []

    for state in range(num_states):
        register_bits = np.array([int(x) for x in np.binary_repr(state, constraint_length - 1)])
        state_transitions = []
        for input_bit in range(2):
            next_state = (state >> 1) | (input_bit << (constraint_length - 2))
            new_register_bits = np.concatenate([[input_bit], register_bits])
            output_A = np.mod(np.sum(new_register_bits * g1), 2)
            output_B = np.mod(np.sum(new_register_bits * g2), 2)
            state_transitions.append({'next_state': next_state, 'output': [output_A, output_B]})
        trellis.append(state_transitions)

    return trellis
