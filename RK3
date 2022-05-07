import math
import numpy as np
import random
import plotly.graph_objs as go


class Conus:
    fig = go.Figure()
    goldenAngle = 2.0 * np.pi * (1.0 - 1.0 / ((1 + 5 ** 0.5) / 2))

    def __init__(self, a, b, c, e):
        # построим конус
        self.a = a
        self.b = b
        self.c = c
        self.e = e
        u = np.linspace(0, c, 100)
        v = np.linspace(0, 2 * np.pi, 100)
        U, V = np.meshgrid(u, v)
        self.X, self.Y, self.Z = U * a * np.cos(V), U * b * np.sin(V), U

        # и его основанием
        self.x_ellipse = U * a * np.cos(V)
        self.y_ellipse = U * b * np.sin(V)
        self.z_ellipse = []
        for i in range(100):
            self.z_ellipse.append(np.repeat(c, 100))
        self.z_ellipse = np.array(self.z_ellipse)

        self.fig.add_surface(x=self.X, y=self.Y, z=self.Z, opacity=0.95, colorscale='Blues')
        self.fig.add_surface(x=self.x_ellipse, y=self.y_ellipse, z=self.z_ellipse, opacity=0.95, colorscale='Blues')
        # opacity = 0.75,
        # self.fig.show()

    def analytics(self):
        S_conus = math.pi * (4 * self.a) * math.sqrt(self.a ** 2 + self.c ** 2) + math.pi * 2 * (self.a + self.b)
        C = (self.N * math.pi * self.e ** 2) / S_conus
        return 1 if C >= 1 else C

    def distribution_points(self, N):
        self.N = N
        S_ellipse = math.pi * 2 * (self.a + self.b)
        S_conus_side = math.pi * (4 * self.a) * math.sqrt(self.a ** 2 + self.c ** 2)
        self.persent = S_ellipse / (S_ellipse + S_conus_side)
        points_on_ellipse = int(N * self.persent)
        points_on_side = int(N - points_on_ellipse)

        I = np.arange(0, points_on_ellipse, dtype=float) + random.uniform(0, 1)
        V = self.goldenAngle * I
        A = np.sqrt(I) / math.sqrt(points_on_ellipse) * self.a
        B = np.sqrt(I) / math.sqrt(points_on_ellipse) * self.b
        self.X = self.c * A * np.cos(V)
        self.Y = self.c * B * np.sin(V)
        self.Z = np.repeat(self.c, points_on_ellipse)
        # self.fig.add_scatter3d(x=self.X, y=self.Y, z=self.Z)

        # точки на стороне
        I = np.arange(0, points_on_side, dtype=float) + random.uniform(0, 1)
        V = self.goldenAngle * I
        A = np.sqrt(I) / math.sqrt(points_on_side) * self.a
        B = np.sqrt(I) / math.sqrt(points_on_side) * self.b
        R = np.linspace(0, self.c, points_on_side)

        self.side_X = R * A * np.cos(V)
        self.side_Y = R * B * np.sin(V)
        self.side_Z = R

    def draw_sphere(self):
        self.X = np.concatenate([self.X, self.side_X])
        self.Y = np.concatenate([self.Y, self.side_Y])
        self.Z = np.concatenate([self.Z, self.side_Z])

        for (x, y, z) in zip(self.X, self.Y, self.Z):
            u = np.linspace(0, np.pi, len(self.X))
            v = np.linspace(0, 2 * np.pi, len(self.X))
            U, V = np.meshgrid(u, v)

            x1 = np.cos(U) * np.sin(V)
            y1 = np.sin(U) * np.sin(V)
            z1 = np.cos(V)

            x1 = self.e * x1 + x
            y1 = self.e * y1 + y
            z1 = self.e * z1 + z
            self.fig.add_surface(x=x1, y=y1, z=z1, opacity=0.9, showscale=False, colorscale='Reds')

    def set_random_point(self, draw):
        if (random.random() < self.persent):
            # на основании
            u = random.uniform(0, 2 * math.pi)
            self.r_x = self.a * np.cos(u)
            self.r_y = self.b * np.sin(u)
            self.r_z = self.c
        else:
            # конус
            u = random.uniform(0, self.c)
            v = random.uniform(0, 2 * math.pi)
            self.r_x = u * self.a * np.cos(v)
            self.r_y = u * self.b * np.sin(v)
            self.r_z = u

        if draw:
            self.fig.add_scatter3d(x=np.array(self.r_x), y=np.array(self.r_y), z=np.array(self.r_z),
                                   marker=dict(opacity=0.9,
                                               reversescale=True,
                                               colorscale='Greens',
                                               size=5),
                                   line=dict(width=0.1),
                                   mode='markers',
                                   name='player 1')
            self.fig.show()

    def distance(self, i):
        return math.sqrt((self.X[i] - self.r_x) ** 2 +
                         (self.Y[i] - self.r_y) ** 2 +
                         (self.Z[i] - self.r_z) ** 2)

    def distants(self):
        for i in range(len(self.X)):
            if self.distance(i) <= self.e:
                return True
        return False


a, b, c, e = 2, 2, 3, 0.2
A = Conus(a, b, c, e)

A.distribution_points(40)
A.draw_sphere()
A.set_random_point(False)

wins_a = 0
games = 1000
print(f"Аналитическое решение {round(A.analytics(), 2)}")
for i in range(1, games + 1):
    A.set_random_point(i == games - 1)
    if A.distants():
        wins_a += 1
    c_g = round(wins_a / i, 2)
    if (i % 100 == 0):
        print(f"i={i}, цена игры={c_g if c_g <= 1 else 1}")
