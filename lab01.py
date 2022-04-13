import numpy
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt

C = numpy.array(
    [
        [12, 5, 4],
        [12, 0, 12],
        [5, 13, 6],
    ]
)

test_C = numpy.array(
    [
        [2, 1, 3],
        [3, 0, 1],
        [1, 2, 1],
    ]
)


def analysis_method(matrix_C):
    numpy.set_printoptions(precision=3)
    u = numpy.array([[1 for _ in range(len(matrix_C))]])
    inv_C = numpy.linalg.inv(matrix_C)
    x = inv_C.dot(u.T) / (u.dot(inv_C).dot(u.T))
    y = u.dot(inv_C) / (u.dot(inv_C).dot(u.T))
    v = 1 / (u.dot(inv_C).dot(u.T))
    print("x:", x.T[0])
    print("y:", y[0])
    print(f"v: {round(v[0][0], 3)}")


def find_max_win_and_min_loss(win, loss, k):
    k_max = numpy.max(win) / (k + 1)
    k_min = numpy.min(loss) / (k + 1)
    return k_max, k_min


def new_strategies(win, loss, k):
    return numpy.argmax(win[k - 1]), numpy.argmin(loss[k - 1])


def new_win_and_loss(matrix_C, win_A, loss_B, k, strategies):
    new_win = [x + y for x, y in zip(matrix_C[:, strategies[k][1]], win_A[k - 1])]
    new_loss = [x + y for x, y in zip(matrix_C[strategies[k][0]], loss_B[k - 1])]
    return new_win, new_loss


def print_table(strategies, win_A, loss_B, max_win, min_loss, e):
    table = PrettyTable(
        ["k", "Выбор А", "Выбор B", "Выигрыш А", "Проигрыш В", "k_max", "k_min", "e"],
        float_format="0.3",
    )
    for k in range(len(strategies)):
        table.add_row(
            [
                k + 1,
                strategies[k][0] + 1,
                strategies[k][1] + 1,
                win_A[k],
                loss_B[k],
                max_win[k],
                min_loss[k],
                e[k],
            ]
        )
    print(table)


def braun_robinson(matrix_C):
    k = 0
    strategies = [[0, 0]]
    win_A = [matrix_C[:, 0].tolist()]
    loss_B = [matrix_C[0].tolist()]
    max_win = []
    min_loss = []
    first_win, first_loss = find_max_win_and_min_loss(win_A, loss_B, k)
    max_win.append(first_win)
    min_loss.append(first_loss)
    e = [min(max_win) - max(min_loss)]
    while e[k] > 0.01:
        k += 1
        strategies.append(new_strategies(win_A, loss_B, k))
        new_win, new_loss = new_win_and_loss(matrix_C, win_A, loss_B, k, strategies)
        win_A.append(new_win)
        loss_B.append(new_loss)

        k_max, k_min = find_max_win_and_min_loss(win_A[k], loss_B[k], k)
        max_win.append(k_max)
        min_loss.append(k_min)

        e.append(min(max_win) - max(min_loss))
    x, y = [], []
    for s in range(len(matrix_C)):
        x.append([row[0] for row in strategies].count(s))
        y.append([row[1] for row in strategies].count(s))
    x = [round(el / len(strategies), 3) for el in x]
    y = [round(el / len(strategies), 3) for el in y]
    v = (min(max_win) + max(min_loss)) / 2

    return np.argmax(x), np.argmax(y), strategies, win_A, loss_B, max_win, min_loss, e, x, y, v


if __name__ == "__main__":
    print("Аналитическое решение:")
    analysis_method(C)
    best_a, best_b, strategies, win_A, loss_B, max_win, min_loss, e, x, y, v = braun_robinson(C)
    # округлить значения до тысячных + вывести вероятности
    print("Численное решение")
    print(f"x: {x}\ny: {y}")
    print(f"v: {round(v, 3)}")

    print_table(strategies, win_A, loss_B, max_win, min_loss, e)
    plt.title("Метод Брауна-Робинсон")  # заголовок
    plt.xlabel("k")  # ось абсцисс
    # plt.ylabel("y")  # ось ординат
    plt.grid()  # включение отображение сетки
    os = list(range(1, len(e) + 1))
    plt.plot(e, color='r', label="e")
    plt.plot(max_win, color='g', label="Верхняя оценка цены игры")
    plt.plot(min_loss, color='b', label="Нижняя оценка цены игры")
    plt.legend()
    # plt.plot(os, e)  # построение графика
    plt.show()

# x, y = [], []
#     for s in range(len(matrix_C)):
#         x.append([row[0] for row in strategies].count(s))
#         y.append([row[1] for row in strategies].count(s))
#     x = [round(el / len(strategies), 3) for el in x]
#     y = [round(el / len(strategies), 3) for el in y]
#     print(x, y)
