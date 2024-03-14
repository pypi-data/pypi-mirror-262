import os
import numpy as np


class MatrixMixin:
    def __str__(self):
        return str(self.data)

    def write_to_file(self, filename):
        np.savetxt(filename, self.data, fmt='%d', delimiter='\t')

    @property
    def shape(self):
        return self.data.shape

    @property
    def transpose(self):
        return Matrix(self.data.T)


class Matrix(MatrixMixin):
    def __init__(self, data):
        self.data = np.array(data)

    def __add__(self, other):
        return Matrix(self.data + other.data)

    def __sub__(self, other):
        return Matrix(self.data - other.data)

    def __mul__(self, other):
        return Matrix(self.data * other.data)

    def __truediv__(self, other):
        return Matrix(self.data / other.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    artifacts_directory = os.path.join(script_directory, "artifacts")
    os.makedirs(artifacts_directory, exist_ok=True)

    # Генерация двух матриц
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (3, 3)))
    matrix2 = Matrix(np.random.randint(0, 10, (3, 3)))

    # Сложение
    result_addition = matrix1 + matrix2
    print("Addition Result:")
    print(result_addition)

    # Вычитание
    result_subtraction = matrix1 - matrix2
    print("\nSubtraction Result:")
    print(result_subtraction)

    # Умножение
    result_multiplication = matrix1 * matrix2
    print("\nMultiplication Result:")
    print(result_multiplication)

    # Покомпонентное деление
    result_elementwise_division = matrix1 / matrix2
    print("\nElementwise Division Result:")
    print(result_elementwise_division)

    # Транспонирование
    transpose_matrix1 = matrix1.transpose
    transpose_matrix2 = matrix2.transpose
    print("\nTranspose Matrix 1:")
    print(transpose_matrix1)
    print("\nTranspose Matrix 2:")
    print(transpose_matrix2)

    # Запись в файл
    file_path_addition = os.path.join(artifacts_directory, "matrix_addition.txt")
    file_path_subtraction = os.path.join(artifacts_directory, "matrix_subtraction.txt")
    file_path_multiplication = os.path.join(artifacts_directory, "matrix_multiplication.txt")
    file_path_elementwise_division = os.path.join(artifacts_directory, "matrix_elementwise_division.txt")

    result_addition.write_to_file(file_path_addition)
    result_subtraction.write_to_file(file_path_subtraction)
    result_multiplication.write_to_file(file_path_multiplication)
    result_elementwise_division.write_to_file(file_path_elementwise_division)

    print(f"\nResults saved to files:")
    print(file_path_addition)
    print(file_path_subtraction)
    print(file_path_multiplication)
    print(file_path_elementwise_division)
