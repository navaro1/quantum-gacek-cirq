import cirq
import numpy as np


class QuantumRandomNumberGenerator:
    measurement_gate_name = 'qrng_measure'
    qubit_name_prefix = 'qrng_'

    def __init__(self, simulator=None):
        if simulator is None:
            simulator = cirq.Simulator()
        self.simulator = simulator

    def generate_binary_array(self, length: int) -> np.ndarray:
        qubits = cirq.NamedQubit.range(length, prefix=QuantumRandomNumberGenerator.qubit_name_prefix)
        h_gates = [cirq.H(qubit) for qubit in qubits]
        measurement_gate = cirq.measure(qubits, key=QuantumRandomNumberGenerator.measurement_gate_name)
        qrng_circuit = cirq.Circuit(h_gates, measurement_gate)
        result = self.simulator.simulate(qrng_circuit)
        return result.measurements[QuantumRandomNumberGenerator.measurement_gate_name]
