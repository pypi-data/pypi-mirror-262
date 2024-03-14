import os
import numpy as np
import hashlib


class HashMixin:
    def __hash__(self):
        hash_object = hashlib.sha256(self.get_data().tobytes())
        return int(hash_object.hexdigest(), 16)

    def cached_multiply(self, other, cache):
        # Используем кэш для проверки, было ли уже вычислено произведение
        key = (self, other)
        if key in cache:
            return cache[key]

        result = self.multiply(other)
        cache[key] = result
        return result


class MatrixMixin:
    @property
    def shape(self):
        return self.get_data().shape

    @property
    def transpose(self):
        return Matrix(self.get_data().T)


class Matrix(MatrixMixin, HashMixin):
    def __init__(self, data):
        self._data = np.array(data)

    def get_data(self):
        return self._data

    def multiply(self, other):
        return Matrix(self.get_data() @ other.get_data())

    def __add__(self, other):
        return Matrix(self.get_data() + other.get_data())

    def __sub__(self, other):
        return Matrix(self.get_data() - other.get_data())

    def __mul__(self, other):
        return Matrix(self.get_data() * other.get_data())

    def __truediv__(self, other):
        return Matrix(self.get_data() / other.get_data())

    def __getitem__(self, key):
        return self.get_data()[key]

    def __setitem__(self, key, value):
        self.get_data()[key] = value


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    artifacts_directory = os.path.join(script_directory, "artifacts")
    os.makedirs(artifacts_directory, exist_ok=True)

    # Генерация матриц A, B, C, D
    np.random.seed(0)
    matrix_A = Matrix(np.random.randint(0, 10, (3, 3)))
    matrix_B = Matrix(np.random.randint(0, 10, (3, 3)))
    matrix_C = Matrix(np.random.randint(0, 10, (3, 3)))
    matrix_D = Matrix(np.random.randint(0, 10, (3, 3)))

    # Сохранение матриц в файлы
    np.savetxt(os.path.join(artifacts_directory, "A.txt"), matrix_A.get_data(), fmt='%d', delimiter='\t')
    np.savetxt(os.path.join(artifacts_directory, "B.txt"), matrix_B.get_data(), fmt='%d', delimiter='\t')
    np.savetxt(os.path.join(artifacts_directory, "C.txt"), matrix_C.get_data(), fmt='%d', delimiter='\t')
    np.savetxt(os.path.join(artifacts_directory, "D.txt"), matrix_D.get_data(), fmt='%d', delimiter='\t')

    # Вычисление и сохранение произведения AB и CD
    cache = {}  # Кэш для произведения матриц
    matrix_AB = matrix_A.cached_multiply(matrix_B, cache)
    matrix_CD = matrix_C.cached_multiply(matrix_D, cache)
    np.savetxt(os.path.join(artifacts_directory, "AB.txt"), matrix_AB.get_data(), fmt='%d', delimiter='\t')
    np.savetxt(os.path.join(artifacts_directory, "CD.txt"), matrix_CD.get_data(), fmt='%d', delimiter='\t')

    # Сохранение хэша матриц AB и CD
    with open(os.path.join(artifacts_directory, "hash.txt"), 'w') as hash_file:
        hash_file.write(f"Hash AB: {hash(matrix_AB)}\n")
        hash_file.write(f"Hash CD: {hash(matrix_CD)}\n")
