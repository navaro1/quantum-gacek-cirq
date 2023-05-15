import cirq

apolonia_qubit = cirq.NamedQubit("Apolonia")

measurement = cirq.measure(apolonia_qubit)

circuit = cirq.Circuit(cirq.H(apolonia_qubit), cirq.measure(apolonia_qubit))
simulator = cirq.Simulator()
simulation_result = simulator.simulate(circuit)

for step, x in enumerate(simulator.simulat128e_moment_steps(circuit)):
    print(f'Step: {step}\nLast moment: {circuit[step]}\nState: {x.state_vector()}\n')