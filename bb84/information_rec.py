import cirq
import numpy as np

# Alice qubits
alice_bit_string = np.array([0, 0, 1])  # x_a
parity_check_matrix = np.array([
    [1, 1, 0],
    [0, 1, 1],
])  # H
alice_syndrome = np.matmul(parity_check_matrix, alice_bit_string)


noise_vector = np.array([0, 0, 0])

bob_received_message = (alice_bit_string + noise_vector) % 2
bob_received_syndrome = np.matmul(parity_check_matrix, bob_received_message)

sum_syndrome = (bob_received_syndrome + alice_syndrome) % 2


def error_estimate(syndrome):
    if np.all(syndrome == np.array([0, 0])):
        return np.array([0, 0, 0])
    elif np.all(syndrome == np.array([0, 1])):
        return np.array([0, 0, 1])
    elif np.all(syndrome == np.array([1, 0])):
        return np.array([1, 0, 0])
    elif np.all(syndrome == np.array([1, 1])):
        return np.array([0, 1, 0])


error_estimate_s = error_estimate(sum_syndrome)
bob_decoded_message = (bob_received_message + error_estimate_s) % 2

print(alice_bit_string)
print(bob_decoded_message)