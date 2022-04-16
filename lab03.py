import numpy as np
import random

np.set_printoptions(precision=3, floatmode='fixed')


def init_matrix(n, min, max):
    return np.random.randint(min, max, (n, n))


def nash(matrix_a, matrix_b):
    # column_max_a = np.argmax(matrix_a, axis=0)
    # row_max_b = np.argmax(matrix_b, axis=1)
    row_max_b = [np.where(row == row.max())[0] for row in matrix_b]
    column_max_a = [np.where(column == column.max())[0] for column in matrix_a.T]
    priemlemo_a = []
    priemlemo_b = []
    for i in range(len(column_max_a)):
        for j in range(len(column_max_a[i])):
            priemlemo_a.append((column_max_a[i][j] + 1, i + 1))
    for i in range(len(row_max_b)):
        for j in range(len(row_max_b[i])):
            priemlemo_b.append((i + 1, row_max_b[i][j] + 1))
    c = list(set(priemlemo_a) & set(priemlemo_a))
    return c


def is_pareto_effective(row, column, matrix_a, matrix_b):
    n=len(matrix_a)
    bool_a = np.empty(shape=(n,n), dtype=bool)
    bool_b = np.empty(shape=(n,n), dtype=bool)
    for i in range(n):
        for j in range(n):
            bool_a[i][j] = matrix_a[i][j] >= matrix_a[row][column]
            bool_b[i][j] = matrix_b[i][j] >= matrix_b[row][column]
            if bool_a[i][j] and bool_b[i][j]:
                if matrix_a[i][j] > matrix_a[row][column] or matrix_b[i][j] > matrix_b[row][column]:
                    return False
    return True


def pareto(matrix_a, matrix_b):
    paretto_effective = []
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a)):
            if is_pareto_effective(i, j, matrix_a, matrix_b):
                paretto_effective.append((i + 1, j + 1))
    return paretto_effective


def print_result(a, b, nash_effective, paretto_effective):
    print()
    print('A:')
    for el in a:
        print(el, sep='\n')
    print()
    print('B:')
    for el in b:
        print(el, sep='\n')
    print()
    print("Эффективно по Нэшу:")
    print(", ".join(repr(e) for e in nash_effective))
    print()
    print("Парето эффективны:")
    print(", ".join(repr(e) for e in paretto_effective))


if __name__ == "__main__":
    # a, b = init_matrix()
    a, b = init_matrix(10, -50, 50), init_matrix(10, -50, 50)

    nash_effective = nash(a, b)
    paretto_effective = pareto(a, b)
    print_result(a, b, nash_effective, paretto_effective)

    # a = np.array([
    #     [1, 4, 7],
    #     [2, 0, 0],
    #     [2, 0, 0],
    # ]
    # )
    # b = np.array([[0, 0, 0],
    #               [5, 1, 2],
    #               [5, 3, 5]])
