import cirq
import numpy as np

apolonia_qubit = cirq.NamedQubit("Apolonia")

measurement = cirq.measure(apolonia_qubit)

circuit = cirq.Circuit(cirq.H(apolonia_qubit))
simulator = cirq.Simulator()
simulation_result = simulator.simulate(circuit)

print(circuit)
print(simulation_result.final_state_vector)

print(np.linalg.norm(simulation_result.final_state_vector))
#
# for step, x in enumerate(simulator.simulate_moment_steps(circuit)):
#     print(f'Step: {step}\nLast moment: {circuit[step]}\nState: {x.state_vector()}\n')