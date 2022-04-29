import numpy as np
import random
from colorama import Fore, Style

np.set_printoptions(precision=2, floatmode='fixed')


def get_stochastic_matrix(size):
    stochastic_matrix = list()
    for i in range(size):
        random_vector = [abs(random.random()) for i in range(size)]
        random_vector_sum = sum(random_vector)
        random_vector = [i / random_vector_sum for i in random_vector]
        stochastic_matrix.append(random_vector)
    return np.array(stochastic_matrix)


def impact(A, x, e):
    stop = False
    i = 0
    while not stop:
        x = A.dot(x)
        stop = all(abs(x[0] - el) <= e for el in x[1:])
        i += 1
    return x, i


def get_agents(size):
    all_agents = [i for i in range(size)]
    agents = []
    while len(agents) < 2:
        for ag in all_agents:
            if random.random() < 0.5 and ag not in agents:
                agents.append(ag)
    random.shuffle(agents)
    sep = random.randint(1, len(agents) - 1)
    agents_1 = agents[:sep]
    agents_2 = agents[sep:]
    return agents_1, agents_2


def print_answer(matrix, x, i_1, x_r, ag_1, ag_2, new_opinion, u, v, new_x, i_2):
    ag_1 = sorted(ag_1)
    ag_2 = sorted(ag_2)
    print("Матрица доверия", matrix, sep='\n', end='\n\n')
    print("Начальный вектор мнений агентов:", f"X={x}", sep='\n', end='\n\n')
    print(f"Результирующие мнения агентов (без влияния) после {i_1} итераций:", f"X={x_r}", sep='\n', end='\n\n')
    print(Fore.GREEN, f"Номера агентов первого игрока: {[i + 1 for i in ag_1]}", Style.RESET_ALL)
    print(Fore.RED, f"Номера агентов второго игрока: {[i + 1 for i in ag_2]}", Style.RESET_ALL)
    print(f"Управление первого игрока: {u}")
    print(f"Управление второго игрока: {v}")
    print("Мнения агентов:")
    for i in range(len(new_opinion)):
        if i in ag_1:
            print(Fore.GREEN, new_opinion[i], Style.RESET_ALL, end=' ')
        elif i in ag_2:
            print(Fore.RED, new_opinion[i], Style.RESET_ALL, end=' ')
        else:
            print(new_opinion[i], Style.RESET_ALL, end=' ')
    print()
    print(f"Результирующие мнения агентов после {i_2} итераций:", f"X={new_x}", sep='\n', end='\n\n')
    if new_x[0] > 0:
        print(Fore.GREEN, f"Победил первый игрок", Style.RESET_ALL)
    else:
        print(Fore.RED, f"Победил второй игрок", Style.RESET_ALL)


def information_confrontation(size):
    stochastic_matrix = get_stochastic_matrix(size=size)
    e = 0.000001
    opinions = np.array([random.randint(1, 20) for _ in range(size)])
    x_r, i_1 = impact(stochastic_matrix, opinions, e)
    agents_1, agents_2 = get_agents(size)
    u = random.randint(0, 100)
    v = random.randint(-100, 0)
    new_opinions = np.array([random.randint(1, 20) for _ in range(size)])
    for ag in agents_1:
        new_opinions[ag] = u
    for ag in agents_2:
        new_opinions[ag] = v
    new_x, i_2 = impact(stochastic_matrix, new_opinions, e)
    print_answer(stochastic_matrix, opinions, i_1, x_r, agents_1, agents_2, new_opinions, u, v, new_x, i_2)


if __name__ == "__main__":
    size = 10
    information_confrontation(size=size)
