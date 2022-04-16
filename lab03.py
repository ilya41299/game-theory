import numpy as np
import data_matrix
from  colorama import Fore, Style

np.set_printoptions(precision=1, floatmode='fixed')


def init_matrix(n, min, max):
    return np.random.randint(min, max, (n, n))


def nash(matrix_a, matrix_b):
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

    return list(set(priemlemo_a).intersection(set(priemlemo_b)))


def is_pareto_effective(row, column, matrix_a, matrix_b):
    n = len(matrix_a)
    bool_a = np.empty(shape=(n, n), dtype=bool)
    bool_b = np.empty(shape=(n, n), dtype=bool)
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


def print_result(a, b, nash_effective, paretto_effective, name):
    print(Fore.CYAN, name, Style.RESET_ALL, end="\n\n")
    print('A:')
    for el in a:
        print(el, sep='\n')
    print()
    print('B:')
    for el in b:
        print(el, sep='\n')
    print()
    print("Равновесие Нэша:", ", ".join(repr(e) for e in nash_effective))

    print("Оптимальность по Парето:", ", ".join(repr(e) for e in paretto_effective), end="\n\n")


def algorithms(a, b, name):
    nash_effective = nash(a, b)
    paretto_effective = pareto(a, b)
    print_result(a, b, nash_effective, paretto_effective, name)


def get_strategies(A, B):
    u = np.ones(len(A))
    inv_A = np.linalg.inv(A)
    inv_B = np.linalg.inv(B)
    u1 = 1 / u.dot(inv_A).dot(u)
    u2 = 1 / u.dot(inv_B).dot(u)
    x = np.dot(u2, u).dot(inv_B)
    y = np.dot(u1, inv_A).dot(u)
    return x, y, round(u1,2), round(u2,1)


def bimatrix_game(a, b):
    nash_strategies = nash(a, b)
    nash_count = len(nash_strategies)
    print(Fore.CYAN, "Биматричная игра", Style.RESET_ALL, end="\n\n")
    print("A:")
    for el in a:
        print(el, sep='\n')
    print()
    print("B:")
    for el in b:
        print(el, sep='\n')
    print()
    if nash_count == 1:
        print(f"Единственная ситуация равновесия по Нэшу: {nash_strategies}")
        return
    elif nash_count == 0:
        print(f"Равновесий по Нэшу в чистых стратегиях нет. Вполне смешанная ситуация равновесия:")

    elif nash_count == 2:
        print(f"Есть две равновесные по Нэшу чистые стратегии:")
    x, y, u1, u2 = get_strategies(a, b)
    print(", ".join(repr(e) for e in nash_strategies))
    print("Вполне смешанная ситуация равновесия:")
    print(f"x={x}, y={y}")
    print("Цена игры:")
    print(f"u1={u1}, u2={u2}")





if __name__ == "__main__":
    algorithms(data_matrix.Matrix_A, data_matrix.Matrix_B, "Для случайной матрицы 10x10")
    algorithms(data_matrix.zk_a, data_matrix.zk_b, "Дилемма заключенного")
    algorithms(data_matrix.crossroads_a, data_matrix.crossroads_b, "Перекресток")
    algorithms(data_matrix.family_dispute_a, data_matrix.family_dispute_b, "Семейный спор")

    bimatrix_game(data_matrix.bimatrix_a, data_matrix.bimatrix_b)
