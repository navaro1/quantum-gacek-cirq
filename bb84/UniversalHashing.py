import numpy as np
import random


class TwoUniversalHash:
    def __init__(self, input_len, output_len, load_factor=1, seed=None):
        self.input_len = input_len
        self.output_len = output_len
        self.load_factor = load_factor
        self.m = int(output_len * load_factor)
        self.seed = seed if seed is not None else random.randint(0, 2 ** 32 - 1)
        self.matrices = self._generate_random_matrices()

    def _generate_random_matrices(self):
        np.random.seed(self.seed)
        matrices = []
        for _ in range(self.output_len):
            matrix = np.random.randint(0, 2, size=(self.input_len, self.m), dtype=np.uint8)
            matrices.append(matrix)
        return matrices

    def hash(self, input_array):
        if len(input_array) != self.input_len:
            raise ValueError(f"Input array length must be {self.input_len}")

        output_array = np.zeros(self.output_len, dtype=np.uint8)
        for i in range(self.output_len):
            product = np.dot(input_array, self.matrices[i]) % 2
            output_array[i] = np.sum(product) % 2

        return output_array

#
# # Usage
# input_len = 10
# output_len = 8
# load_factor = 1
# seed = 42
#
# hash_function = TwoUniversalHash(input_len, output_len, load_factor, seed)
# input_array = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], dtype=np.uint8)
# hashed_array = hash_function.hash(input_array)
# print("Hashed array:", hashed_array)
