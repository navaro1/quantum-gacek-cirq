from abc import ABC, abstractmethod

import numpy as np
import cirq


class RandomNumberGenerator(ABC):

    @abstractmethod
    def generate_binary_array(self, length: int) -> np.ndarray:
        pass


class ClassicalRandomNumberGenerator(RandomNumberGenerator):

    def generate_binary_array(self, length: int) -> np.ndarray:
        return np.random.randint(0, 2, size=length)


class QuantumRandomNumberGenerator(RandomNumberGenerator):

    def generate_binary_array(self, length: int) -> np.ndarray:
        qubits = cirq.NamedQubit.range(length, prefix=f"rng_")
        h_gates = [cirq.H(q) for q in qubits]
        measurement_gate = cirq.measure(qubits, key='m')
        rng_circuit = cirq.Circuit(h_gates, measurement_gate)
        result = cirq.Simulator().simulate(rng_circuit)
        return result.measurements['m']


qrg = QuantumRandomNumberGenerator()

print(qrg.generate_binary_array(3))
