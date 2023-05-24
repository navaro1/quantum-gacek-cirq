import cirq
import numpy as np

from Notebooks.quantum_lib.qrng import QuantumRandomNumberGenerator

# Step 1
simulator = cirq.Simulator()
qrng = QuantumRandomNumberGenerator()

np.random.seed(300)

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

# Introducing Eve!
print("=============Introducing Eve==============")
alice_quantum_channel = cirq.Circuit()
alice_qubits = cirq.NamedQubit.range(string_length, prefix="aq_")
for idx in range(string_length):
    if alice_a[idx] == 1:
        alice_quantum_channel.append(cirq.X(alice_qubits[idx]))
    if alice_b[idx] == 1:
        alice_quantum_channel.append(cirq.H(alice_qubits[idx]))

# EVE!!!
eve_b = qrng.generate_binary_array(string_length)
for idx in range(string_length):
    if eve_b[idx] == 1:
        alice_quantum_channel.append(cirq.H(alice_qubits[idx]))

alice_quantum_channel.append(cirq.measure(alice_qubits, key="eve_measurement"))
eve_simulation_result = simulator.simulate(alice_quantum_channel)
eve_guess_decode = eve_simulation_result.measurements["eve_measurement"]

# Eve creates message sneakily
eve_quantum_channel = cirq.Circuit()
eve_qubits = cirq.NamedQubit.range(string_length, prefix="eq_")
for idx in range(string_length):
    if eve_guess_decode[idx] == 1:
        eve_quantum_channel.append(cirq.X(eve_qubits[idx]))
    if eve_b[idx] == 1:
        eve_quantum_channel.append(cirq.H(eve_qubits[idx]))

# Now Bob takes the measurements
for idx in range(string_length):
    if bob_b[idx] == 1:
        eve_quantum_channel.append(cirq.H(alice_qubits[idx]))

eve_quantum_channel.append(cirq.measure(alice_qubits, key="bob_measurement"))
bob_simulation_result = simulator.simulate(eve_quantum_channel)
bob_guess_decode = bob_simulation_result.measurements["bob_measurement"]
print("Bob:", "Hey Alice, I received and measured state you've sent me!")

print("Alice b string:", alice_b)
print("Eve b string:  ", eve_b)
print("Bob b string:  ", bob_b, "\n")

print("Alice a string:    ", alice_a)
print("Eve decoded string:", eve_guess_decode)
print("Bob decoded string:", bob_guess_decode)

b_matching_indices = alice_b == bob_b
alice_kept_a = alice_a[b_matching_indices]
bob_kept_a = bob_guess_decode[b_matching_indices]

print("Alice kept:", alice_kept_a)
print("Bob kept:  ", bob_kept_a)

# Step 5
test_indices = []
while len(test_indices) != 4:
    test_indices_source = qrng.generate_binary_array(len(alice_kept_a))
    test_indices = np.where(test_indices_source == 1)[0]
print(f"Hey Bob, here are the test indices: {test_indices}")
alice_test_a = alice_kept_a[test_indices]
bob_test_a = bob_kept_a[test_indices]

threshold = 1
not_matching_elements = len(np.where(alice_test_a != bob_test_a))
if not_matching_elements > threshold:
    print("Restart the protocol!")
else:
    print("Continue!")

final_indices = np.where(test_indices_source == 0)[0]
alice_final_a = alice_kept_a[final_indices]
bob_final_a = bob_kept_a[final_indices]
print(alice_final_a)
print(bob_final_a)

# encode(a + b) = encode(a) + encode(b)
# bob_final_a == alice_final_a + some_noise
# encode(alice_final_a)
# encode(bob_final_a) == encode(alice_final_a + some_noise)
#   == encode(alice_final_a) + encode(some_noise)
# encode(bob_final_a) - encode(alice_final_a) == encode(some_noise)
# alice_final_a !!

# 2-universal hashing