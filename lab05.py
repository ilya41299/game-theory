from itertools import combinations
import math
from colorama import Fore, Style


def create_omega(N, gain):
    s_to_vs = dict()
    omega = list()
    gamers = [i for i in range(1, N + 1)]
    gain_index = 0
    for size in range(0, N + 1):
        subsets = [j for j in combinations(gamers, size)]
        for subset in subsets:
            subset = set([el for el in subset])
            omega.append(subset)
            s_to_vs[str(subset)] = gain[gain_index]
            gain_index += 1
    return omega, s_to_vs


def get_v_shapley(omega, s_to_vs, N):
    x = list()
    for i in range(1, N + 1):
        sum_by_subset = 0
        for subset in omega:
            if i not in subset:
                continue
            modul_subset = len(subset)
            N_minus_modul_subset = N - modul_subset
            delta = s_to_vs[str(subset)] - s_to_vs[str(subset - {i})]
            sum_by_subset += math.factorial(modul_subset - 1) * math.factorial(N_minus_modul_subset) * delta
        x.append(sum_by_subset / math.factorial(N))
    return x


def is_superadditive(omega_o, s_to_vs):
    superadditive = True
    omega = omega_o[1:]
    print(Fore.MAGENTA, "Проверка супераддитивности игры", Style.RESET_ALL)
    for pair in combinations(omega, 2):
        if pair[0] & pair[1] == set():
            formula = f"V{pair[0] | pair[1]} >= V{pair[0]} + V{pair[1]}"
            value = f"{s_to_vs[str(pair[0] | pair[1])]} >= {s_to_vs[str(pair[0])]} + {s_to_vs[str(pair[1])]}"
            if s_to_vs[str(pair[0] | pair[1])] < s_to_vs[str(pair[0])] + s_to_vs[str(pair[1])]:
                superadditive = False
                print(Fore.RED, "Игра не является супераддитивной", Style.RESET_ALL)
                print('{color} {:<{size}}'.format(formula, color=Fore.RED, size=40), end='      ')
                print('{color} {:<{size}}'.format(value, color=Fore.RED, size=20))
                print(''.format(color=Fore.RESET))
                return False
            else:
                print('{color} {:<{size}}'.format(formula, color=Fore.RESET, size=40), end='      ')
                print('{color} {:<{size}}'.format(value, color=Fore.RESET, size=20))
    print(Fore.GREEN, "Игра является супераддитивной", Style.RESET_ALL, end="\n\n")
    return superadditive


def is_convexity(omega_o, s_to_vs):
    omega = omega_o[1:]
    is_convexity_ = True
    print(Fore.MAGENTA, "Проверка выпуклости игры", Style.RESET_ALL)
    for pair in combinations(omega, 2):
        union = pair[0] | pair[1]
        intersection = pair[0] & pair[1]
        formula = f"V{union} + V{intersection} >= V{pair[0]} + V{pair[1]}"
        value = f"{s_to_vs[str(union)]} + {s_to_vs[str(intersection)]} >= {s_to_vs[str(pair[0])]} + {s_to_vs[str(pair[1])]}"
        if s_to_vs[str(union)] + s_to_vs[str(intersection)] < s_to_vs[str(pair[0])] + s_to_vs[str(pair[1])]:
            is_convexity_ = False
            # print(Fore.RED, string, Style.RESET_ALL)
            print('{color} {:<{size}}'.format(formula, color=Fore.RED, size=60), end='      ')
            print('{color} {:<{size}}'.format(value, color=Fore.RED, size=20))
        else:
            print('{color} {:<{size}}'.format(formula, color=Fore.RESET, size=60), end='      ')
            print('{color} {:<{size}}'.format(value, color=Fore.RESET, size=20))
    print(Fore.GREEN, "Игра является выпуклой", Style.RESET_ALL) if is_convexity_ else print(Fore.RED,
                                                                                             "Игра не является выпуклой",
                                                                                             Style.RESET_ALL)
    print()


def group_rationalization(shapley, omega, s_to_vs):
    print(Fore.MAGENTA, "Проверка условия групповой рационализации", Style.RESET_ALL)
    shapley_ = [round(el, 2) for el in shapley]
    print(f"Вектор Шепли: X={shapley_}")
    print(f"{sum(shapley)} = V{omega[len(omega) - 1]} = {float(s_to_vs[str(omega[len(omega) - 1])])}")
    if (sum(shapley) == float(s_to_vs[str(omega[len(omega) - 1])])):
        print(Fore.GREEN, "Условие групповой рационализации выполняется", Style.RESET_ALL)
    else:
        print(Fore.RED, "Условие групповой рационализации не выполняется", Style.RESET_ALL)
    print()


def individual_rationalization(shapley, s_to_vs, N):
    shapley_ = [round(el, 2) for el in shapley]
    print(Fore.MAGENTA, "Проверка условия индивидуальной рационализации", Style.RESET_ALL)
    flag = True
    for i in range(1, N + 1):
        if shapley[i - 1] >= s_to_vs[str({i})]:
            print(f"X{i}(V)= {shapley_[i - 1]} >= {s_to_vs[str({i})]}")
        else:
            print(Fore.RED, f"X{i}(V)= {shapley_[i - 1]} >= {s_to_vs[str({i})]}", Style.RESET_ALL)
            flag = False
    if flag:
        print(Fore.GREEN, "Условие индивидуальной рационализации выполняется", Style.RESET_ALL)
    else:
        print(Fore.RED, "Условие индивидуальной рационализации НЕ выполняется", Style.RESET_ALL)


if __name__ == "__main__":
    N = 4
    gain = [0, 2, 1, 1, 2, 4, 4, 4, 2, 4, 4, 7, 8, 8, 6, 10]
    omega, s_to_vs = create_omega(N, gain)
    if is_superadditive(omega, s_to_vs):
        shapley = get_v_shapley(omega, s_to_vs, N)
        is_convexity(omega, s_to_vs)
        group_rationalization(shapley, omega, s_to_vs)
        individual_rationalization(shapley, s_to_vs, N)
  
