# -*- coding:Utf-8 -*-

import tkinter as tk
from file2 import calculate_new_vectors
import numpy as np
import numpy.random as rd
from math import sqrt
from random import randrange

root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root)
canvas.pack(expand=True, fill='both')

size = 8

sw = root.winfo_screenwidth()
w = sw - size
sh = root.winfo_screenheight()
h = sh - size

# n = 500
# a = np.empty((n, 4), dtype=np.float64)
# a[:, :2] = rd.randint(0, 120, (n, 2)) * 10
# a_ = rd.randint(0, 50, (n,))
# a[:, 2:] = np.array((a_, np.sqrt(50 ** 2 - a_ ** 2))).T


ax = np.arange(0, w, size ** 2)
ay = np.arange(0, h, size ** 2)
a = np.empty((ax.shape[0] * ay.shape[0], 4), dtype=np.float64)
i = 0
print(ax.shape, ay.shape)
for x in ax:
    for y in ay:
        vx = randrange(-50, 51)
        a[i] = x, y, vx, sqrt(2500 - vx ** 2)
        i += 1

n = ax.shape[0] * ay.shape[0]
# previous_collisions_array = np.zeros(n, dtype=np.bool)

# n = 2
# a = np.array((
#     (25, 200, 50, 0),
#     (90, 100, 40, 30)
#               ), dtype=np.float64)

# a = np.array((
#     (45, 250, 50, 0),
#     (150, 200, 30, 20)
#               ), dtype=np.float64)


entities = dict()
for i in range(n):
    v = a[i]
    entities[canvas.create_oval(*v[:2] - size, *v[:2] + size)] = i

# distance = sqrt(size ** 2 + size ** 2) * 2

paused = False
collision_distance = size * 2
squared_collision_distance = collision_distance ** 2


def pause(*_):
    global paused
    paused = True


def move_entity(*_):
    global a, paused
    a = calculate_new_vectors(a, collision_distance, squared_collision_distance)
    for entity, i in entities.items():
        pos = a[i, :2]
        if pos[1] > h:
            a[i, 3] = -np.abs(a[i, 3])
        if pos[1] < size:
            a[i, 3] = np.abs(a[i, 3])
        if pos[0] > w:
            a[i, 2] = -np.abs(a[i, 2])
        if pos[0] < size:
            a[i, 2] = np.abs(a[i, 2])
        a[i, :2] += a[i, 2:] / 30
        canvas.coords(entity, *a[i, :2] - size, *a[i, :2] + size)
    if not paused:
        canvas.after(8, move_entity)
    else:
        paused = False


def velocity_sum(*args):
    array = np.sqrt(np.abs(a[:, 2] ** 2) + np.abs(a[:, 3] ** 2))
    print(np.sum(array))


canvas.bind('<space>', move_entity)
canvas.bind('p', pause)
canvas.bind('a', velocity_sum)
canvas.focus_set()
root.mainloop()
