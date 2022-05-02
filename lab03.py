import numpy as np
import data_matrix
from colorama import Fore, Style

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
    pareto_effective = []
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a)):
            if is_pareto_effective(i, j, matrix_a, matrix_b):
                pareto_effective.append((i + 1, j + 1))
    return pareto_effective


def print_result(a, b, nash_effective, pareto_effective, name):
    print(Fore.CYAN, name, Style.RESET_ALL, end="\n\n")

    for i in range(len(a)):
        for j in range(len(a)):
            if any([nash[0] == i + 1 and nash[1] == j + 1 for nash in nash_effective]) and any(
                    [pareto[0] == i + 1 and pareto[1] == j + 1 for pareto in pareto_effective]):
                print('{color} {:^{size}}'.format(f"{a[i][j]}/{b[i][j]}", color=Fore.BLUE, size=8), end='')
            elif any([nash[0] == i + 1 and nash[1] == j + 1 for nash in nash_effective]):
                print('{color} {:^{size}}'.format(f"{a[i][j]}/{b[i][j]}", color=Fore.RED, size=8), end='')
            elif any([pareto[0] == i + 1 and pareto[1] == j + 1 for pareto in pareto_effective]):
                print('{color} {:^{size}}'.format(f"{a[i][j]}/{b[i][j]}", color=Fore.GREEN, size=8), end='')
            else:
                print('{color} {:^{size}}'.format(f"{a[i][j]}/{b[i][j]}", color=Fore.RESET, size=8), end='')
        print('\n')

    print(Fore.RED, "Равновесие Нэша:", Style.RESET_ALL, end="")
    print(", ".join(repr(e) for e in nash_effective))

    print(Fore.GREEN, "Оптимальность по Парето:", Style.RESET_ALL, end="")
    print(", ".join(repr(e) for e in pareto_effective), end="\n")

    intersection = list(set(pareto_effective).intersection(set(nash_effective)))
    if intersection:
        print(Fore.BLUE, "Пересечение:", Style.RESET_ALL, end="")
        print(", ".join(repr(e) for e in intersection), end="\n")
    print('\n')


def algorithms(a, b, name):
    nash_effective = nash(a, b)
    pareto_effective = pareto(a, b)
    print_result(a, b, nash_effective, pareto_effective, name)


def get_strategies(A, B):
    u = np.ones(len(A))
    inv_A = np.linalg.inv(A)
    inv_B = np.linalg.inv(B)
    u1 = 1 / u.dot(inv_A).dot(u)
    u2 = 1 / u.dot(inv_B).dot(u)
    x = np.dot(u2, u).dot(inv_B)
    y = np.dot(u1, inv_A).dot(u)
    return x, y, round(u1, 2), round(u2, 1)


def bimatrix_game(a, b):
    nash_strategies = nash(a, b)
    nash_count = len(nash_strategies)
    print(Fore.CYAN, "Биматричная игра", Style.RESET_ALL, end="\n")
    for i in range(len(a)):
        for j in range(len(a)):
            if any([nash[0] == i + 1 and nash[1] == j + 1 for nash in nash_strategies]):
                print('{color} {:^{size}}'.format(f"{a[i][j]}/{b[i][j]}", color=Fore.MAGENTA, size=8), end='')
            else:
                print('{color} {:^{size}}'.format(f"{a[i][j]}/{b[i][j]}", color=Fore.RESET, size=8), end='')
        print('\n')
    if nash_count == 1:
        print(Fore.MAGENTA, f"Единственная ситуация равновесия по Нэшу: {nash_strategies}", Style.RESET_ALL, end="")
        print()
        return
    elif nash_count == 0:
        print(Fore.MAGENTA, f"Равновесий по Нэшу в чистых стратегиях нет. Вполне смешанная ситуация равновесия:",
              Style.RESET_ALL, end="")

    elif nash_count == 2:
        print(Fore.MAGENTA, f"Есть две равновесные по Нэшу чистые стратегии:", Style.RESET_ALL, end="")
    x, y, u1, u2 = get_strategies(a, b)
    print(", ".join(repr(e) for e in nash_strategies))
    print(f" Вполне смешанная ситуация равновесия: x={x}, y={y}")
    print(f" Цена игры: u1={u1}, u2={u2}")


if __name__ == "__main__":
    n_=10
    min_=-10
    max_=10
    random_matrix_A = init_matrix(n=n_, min=min_, max=max_)
    random_matrix_B = init_matrix(n=n_, min=min_, max=max_)
    algorithms(random_matrix_A, random_matrix_B, "Случайная матрицы 10x10")
    # algorithms(data_matrix.Matrix_A, data_matrix.Matrix_B, "Случайная матрицы 10x10")
    algorithms(data_matrix.zk_a, data_matrix.zk_b, "Дилемма заключенного")
    algorithms(data_matrix.crossroads_a, data_matrix.crossroads_b, "Перекресток")
    algorithms(data_matrix.family_dispute_a, data_matrix.family_dispute_b, "Семейный спор")

    bimatrix_game(data_matrix.bimatrix_a, data_matrix.bimatrix_b)
