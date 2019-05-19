# -*- coding:Utf-8 -*-

import tkinter as tk
from file2 import calculate_new_vectors
import numpy as np
import numpy.random as rd
import math
sqrt = math.sqrt

root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root)
canvas.pack(expand=True, fill='both')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
# n = 500
# a = np.empty((n, 4), dtype=np.float64)
# a[:, :2] = np.arange(1000).reshape((500, 2)) * 10
# a_ = rd.randint(0, 50, (n,))
# a[:, 2:] = np.array((a_, np.sqrt(50 ** 2 - a_ ** 2))).T


class Molecule:

    def __init__(self, coords, angle, velocity, index, array):
        self.index = index
        self.array = array

        array[index] = coords[0], coords[1], angle, velocity

    def _get_x(self):
        return self.array[self.index][0]

    def _set_x(self, value):
        self.array[self.index][0] = value

    def _get_y(self):
        return self.array[self.index][1]

    def _set_y(self, value):
        self.array[self.index][1] = value

    def _get_angle(self):
        return self.array[self.index][2]

    def _set_angle(self, value):
        self.array[self.index][2] = value

    def _get_v(self):
        return self.array[self.index][3]

    def _set_v(self, value):
        self.array[self.index][3] = value

    def update(self):
        self.x += math.cos(self.angle) * self.velocity
        self.y += math.sin(self.angle) * self.velocity

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    angle = property(_get_angle, _set_angle)
    velocity = property(_get_v, _set_v)


a = np.empty((100, 4), dtype=np.int32)

molecules = list()
n = 100
for i in range(n):
    molecules.append(Molecule((i * 10, 0), 0, 50, i, a))


# n = 2
# a = np.array((
#     (25, 200, 50, 0),
#     (90, 100, 40, 30)
#               ), dtype=np.float64)

# a = np.array((
#     (45, 250, 50, 0),
#     (150, 200, 40, 30)
#               ), dtype=np.float64)


size = 8
entities = dict()
for i in range(n):
    v = a[i]
    entities[canvas.create_oval(*v[:2] - size, *v[:2] + size)] = i

distance = sqrt(size ** 2 + size ** 2) * 2


def move_entity(*args):
    global a
    a = calculate_new_vectors(a, size * 2)
    for entity, i in entities.items():
        pos = a[i, :2]
        if pos[1] > 1200:
            a[i, 3] = -np.abs(a[i, 3])
        if pos[1] < 0:
            a[i, 3] = np.abs(a[i, 3])
        if pos[0] > 1800:
            a[i, 2] = -np.abs(a[i, 2])
        if pos[0] < 0:
            a[i, 2] = np.abs(a[i, 2])
        a[i, :2] += a[i, 2:] / 50
        canvas.coords(entity, *a[i, :2] - size, *a[i, :2] + size)
    canvas.after(10, move_entity)


def velocity_sum(*args):
    array = np.sqrt(np.abs(a[:, 2] ** 2) + np.abs(a[:, 3] ** 2))
    print(np.sum(array))


canvas.bind('<space>', move_entity)
canvas.bind('a', velocity_sum)
canvas.focus_set()
root.mainloop()
