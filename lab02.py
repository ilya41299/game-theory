import numpy as np
import lab01


def analysis_method():
    a, b, c, d, e = -5, 9 / 2, 15, -9 / 2, -9

    x = (c * e - 2 * b * d) / (4 * a * b - c ** 2)
    y = (-c * x - e) / (2 * b)
    print(f"Аналитическое решение: H(x,y)= {H(x, y)}")


def H(x, y):
    return -5 * x ** 2 + (9 / 2) * y ** 2 + 15 * x * y + (-9 / 2) * x + (-9) * y
    # return -3 * x ** 2 + (3 / 2) * y ** 2 + (18 / 5) * x * y + (-18 / 50) * x + (-72 / 25) * y


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


def compute():
    N = 2
    H_queue = []
    while N <= 7 or len(set(H_queue)) != 1:
        matrix = kernel(N)
        i, j, saddle_value = saddle_point(matrix)
        if i == -1:
            i, j, *_ = lab01.braun_robinson(matrix)
            saddle_value = matrix[i][j]
        # print(matrix)
        for row in range(0, len(matrix)):
            for column in range(0, len(matrix)):
                matrix[row][column] = round(matrix[row][column], 2)
        print(f"N={N}")
        print(matrix)
        print(f'x = {round(i / N, 3)}, y = {round(j / N, 2)}, H = {round(saddle_value, 3)}\n')

        N += 1
        H_queue.append(round(saddle_value, 3))
        if len(H_queue) > 5:
            H_queue.pop(0)


analysis_method()
print(f"Численное решение:")
compute()
