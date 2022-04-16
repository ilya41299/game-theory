import numpy as np

Matrix_A = np.array(
    [[24, 2, 40, -46, 27, -46, 35, -23, -33, -50],
     [-40, 28, -15, 38, 26, -38, -35, -26, -37, -19],
     [-1, -36, 30, -35, 4, 7, 17, -6, -8, -33],
     [46, 1, 2, -48, 45, -3, -29, -24, 36, 24],
     [-9, 41, -9, -17, -30, -20, -44, 41, -43, 9],
     [19, 49, 0, -30, -48, 38, -18, -27, 35, 11],
     [37, 4, -9, -7, -21, -9, 15, -49, -23, -20],
     [-33, 29, -29, 24, -21, 17, 49, 41, -36, 40],
     [-40, 24, -45, 49, 1, 47, 49, -17, 26, -15],
     [46, 9, 28, -38, -11, 32, 9, 42, 19, 37]])

Matrix_B = np.array([[32, 2, 17, -29, -42, -8, -20, -16, 12, -1],
                     [-11, -22, -47, 49, -25, 26, 35, 30, 23, -30],
                     [46, -14, -17, 5, -22, -33, -2, -15, -48, -14],
                     [28, -6, 18, -38, 49, -28, 37, 7, 17, -19],
                     [25, -48, 6, -22, 12, -5, -32, -35, 42, -33],
                     [13, -37, -10, 39, -16, 42, -31, -6, -16, -43],
                     [10, -38, 36, -30, 5, -9, -30, 34, 43, -15],
                     [37, 23, 5, 17, 49, -30, 47, 8, 6, 34],
                     [9, -32, 41, 34, -12, 43, -11, -39, 24, -3],
                     [-49, -5, 36, 24, -39, -41, -13, 10, -18, 4]])

zk_a = np.array([
    [-5, 0],
    [-10, -1]
])
zk_b = np.array([
    [-5, -10],
    [0, -1]
])

crossroads_a = np.array([[1, 1 - 0.1], [2, 0]])
crossroads_b = np.array([[1, 2], [1 - 0.1, 0]])

family_dispute_a = np.array([[4, 0], [0, 1]])
family_dispute_b = np.array([[1, 0], [0, 4]])
