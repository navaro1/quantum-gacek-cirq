import math

import numpy as np
import cirq

zero_state = np.array([1, 0])
one_state = np.array([0, 1])
plus_state = (zero_state + one_state) / np.sqrt(2)
minus_state = (zero_state - one_state) / np.sqrt(2)

# Step 1: Eve generates stuff
np.random.seed(200)
parameter_n = 6
parameter_delta = 0.23
string_length = round(4 + parameter_delta) * parameter_n
string_a = np.random.randint(0, 2, size=string_length, dtype=np.uint8)
string_b = np.random.randint(0, 2, size=string_length, dtype=np.uint8)

alice_qubits = cirq.NamedQubit.range(string_length, prefix="alice_")
state_preparing_channels = []
for i in range(string_length):
    aa_i = string_a[i]
    ab_i = string_b[i]
    if ab_i == 0 and aa_i == 0:
        state_preparing_array = zero_state
    elif ab_i == 0 and aa_i == 1:
        state_preparing_array = one_state
    elif ab_i == 1 and aa_i == 0:
        state_preparing_array = plus_state
    elif ab_i == 1 and aa_i == 1:
        state_preparing_array = minus_state

    alice_qubit_i = alice_qubits[i]
    state_preparing_channel_i = cirq.StatePreparationChannel(state_preparing_array, name="State Preperation in: " + str(
        state_preparing_array)).on(alice_qubit_i)
    state_preparing_channels.append(state_preparing_channel_i)

# Bob receives and measures the data
string_b_prim = np.random.randint(0, 2, size=string_length, dtype=np.uint8)
bob_measurements = []
for i in range(string_length):
    abprim_i = string_b_prim[i]
    alice_qubit_i = alice_qubits[i]
    if abprim_i == 1:
        bob_measurements.append(cirq.H(alice_qubit_i))
bob_measurements.append(cirq.measure(alice_qubits, key="bob_measurements"))

quantum_channel = cirq.Circuit(state_preparing_channels, bob_measurements)
result = cirq.Simulator().simulate(quantum_channel)
quantum_measurements_results = result.measurements
string_a_prim = quantum_measurements_results['bob_measurements']
print("Alice String a   :", string_a)
print("Bob string a-prim:", string_a_prim)
print("Alice string b   :", string_b)
print("Bob string b-prim:", string_b_prim)

# Bob tells Alice over the CAC that he received and measured all the qubits.
print("===========================")
# Alice and Bob exchange their basis strings θ and θ˜ over the CAC
matching_bases_array_s = string_b == string_b_prim
alice_string_s = string_a[matching_bases_array_s]
bob_string_s = string_b[matching_bases_array_s]

alice_t = sorted(np.random.choice(len(alice_string_s), math.floor(len(alice_string_s) / 2), replace=False))

alice_x_t = alice_string_s[alice_t]

bob_x_t = bob_string_s[alice_t]
print(alice_x_t)
print(bob_x_t)
