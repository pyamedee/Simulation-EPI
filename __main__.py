# -*- coding:Utf-8 -*-

import tkinter as tk
from file import calculate_new_vectors
import numpy as np
import numpy.random as rd
from math import sqrt

root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root)
canvas.pack(expand=True, fill='both')

n = 500
a = np.empty((n, 4), dtype=np.float64)
a[:, :2] = rd.randint(0, 120, (n, 2)) * 10
a_ = rd.randint(0, 50, (n,))
a[:, 2:] = np.array((a_, np.sqrt(50 ** 2 - a_ ** 2))).T

#
# n = 2
# a = np.array((
#     (25, 200, 50, 0),
#     (90, 100, 40, 30)
#               ), dtype=np.float64)

# a = np.array((
#     (45, 250, 50, 0),
#     (150, 200, 30, 20)
#               ), dtype=np.float64)


size = 5
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
    canvas.after(2, move_entity)


def velocity_sum(*args):
    array = np.sqrt(np.abs(a[:, 2] ** 2) + np.abs(a[:, 3] ** 2))
    print(np.sum(array))


canvas.bind('<space>', move_entity)
canvas.bind('a', velocity_sum)
canvas.focus_set()
root.mainloop()
