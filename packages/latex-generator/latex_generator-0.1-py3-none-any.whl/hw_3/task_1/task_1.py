import os

import numpy as np


class Matrix:
    def __init__(self, data):
        self.data = np.array(data)
        self.shape = self.data.shape

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same dimensions for addition.")
        result_data = self.data + other.data
        return Matrix(result_data)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.shape[1] != other.shape[0]:
                raise ValueError(
                    "Number of columns in the first matrix must be equal to the number of rows in the second matrix "
                    "for matrix multiplication.")
            result_data = np.dot(self.data, other.data)
        else:
            result_data = self.data * other
        return Matrix(result_data)

    def __matmul__(self, other):
        return self.__mul__(other)


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    artifacts_directory = os.path.join(script_directory, "artifacts")
    os.makedirs(artifacts_directory, exist_ok=True)
    # Генерация двух матриц
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    # Сложение, умножение и матричное умножение
    result_addition = matrix1 + matrix2
    result_elementwise_mul = matrix1 * matrix2
    result_matrix_mul = matrix1 @ matrix2

    add_file_path = os.path.join(artifacts_directory, "matrix+.txt")
    mul_file_path = os.path.join(artifacts_directory, "matrix_.txt")
    matmul_file_path = os.path.join(artifacts_directory, "matrix@.txt")
    # Запись результатов в текстовые файлы
    np.savetxt(add_file_path, result_addition.data, fmt='%d', delimiter='\t')
    np.savetxt(mul_file_path, result_elementwise_mul.data, fmt='%d', delimiter='\t')
    np.savetxt(matmul_file_path, result_matrix_mul.data, fmt='%d', delimiter='\t')
