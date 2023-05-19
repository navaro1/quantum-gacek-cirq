import cirq
from Notebooks.quantum_lib.qrng import QuantumRandomNumberGenerator

# Step 1
simulator = cirq.Simulator()
qrng = QuantumRandomNumberGenerator()

n = 4
string_length = 4 * n

alice_a = qrng.generate_binary_array(string_length)
alice_b = qrng.generate_binary_array(string_length)

# Step 2
channel_qubits = cirq.NamedQubit.range(string_length, prefix='q_')
quantum_channel = cirq.Circuit()

for idx in range(string_length):
    if alice_a[idx] == 1:
        quantum_channel.append(cirq.X(channel_qubits[idx]))
    if alice_b[idx] == 1:
        quantum_channel.append(cirq.H(channel_qubits[idx]))

# Step 3
bob_b = qrng.generate_binary_array(string_length)
for idx in range(string_length):
    if bob_b[idx] == 1:
        quantum_channel.append(cirq.H(channel_qubits[idx]))

quantum_channel.append(cirq.measure(channel_qubits, key="bob_measurement"))

simulation_result = simulator.simulate(quantum_channel)
bob_guess_decode = simulation_result.measurements["bob_measurement"]

print("Bob:", "Hey Alice, I received and measured state you've sent me!")

# Step 4
b_matching_indices = alice_b == bob_b
alice_kept_a = alice_a[b_matching_indices]
bob_kept_a = bob_guess_decode[b_matching_indices]

print("Alice b string:", alice_b)
print("Bob b string:  ", bob_b, "\n")
print("Alice a string:    ", alice_a)
print("Bob decoded string:", bob_guess_decode, "\n")
print("Alice kept:", alice_kept_a)
print("Bob kept:  ", bob_kept_a)
