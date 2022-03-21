import numpy as np
import lab01

def H(x, y):
#    result = -5 * x ** 2 + (9 / 2) * y ** 2 + 15 * x * y + (-9 / 2) * x + (-9) * y
    return -3 * x ** 2 + (3 / 2) * y ** 2 + (18/5) * x * y + (-18 / 50) * x + (-72/25) * y


def kernel(N):
    matrix = []
    for i in range(0, N + 1):
        row = []
        for j in range(0, N + 1):
            row.append(H(i / N, j / N))
        matrix.append(row)
    return np.array(matrix)


def saddle_point(matrix):
    # 0 - столбцы, 1 - строки
    row_min = np.min(matrix, axis=0)
    column_max = np.max(matrix, axis=1)
    for i in range(0, len(row_min)):
        for j in range(len(column_max)):
            if row_min[i] == column_max[j]:
                return i, j, row_min[i]
    return -1, -1, -1


def huita():
    N = 2
    while N <= 10:
        matrix = kernel(N)
        i, j, saddle_value = saddle_point(matrix)
        if i == -1:
            i, j, *_ = lab01.braun_robinson(matrix)
            saddle_value = matrix[i][j]
        print(matrix)
        print(f'i = {i}, j = {j}, H = {saddle_value}')

        N+=1


huita()




