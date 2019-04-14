# -*- coding:Utf-8 -*-

import numpy as np
from math import sqrt


def get_distances(array, coords):
    a = np.abs(array - coords)
    a **= 2
    return np.sqrt(a[:, 0] + a[:, 1])


def calculate_new_vectors(a, collision_distance):
    pairs = dict()
    for i in range(a.shape[0]):
        position = a[i, :2]
        distances = get_distances(a[:, :2], position)
        valids = (distances < collision_distance).nonzero()[0]
        for valid in (v for v in valids if v != i):
            if pairs.get(i, None) is None:
                pairs[valid] = i
                x1, y1, vx1, vy1 = a[i]
                x2, y2, vx2, vy2 = a[valid]

                # pv1 = np.array(((x2 - x1), (y2 - y1)))
                vvr1 = np.array((vx2 - vx1, vy2 - vy1))
                vvr2 = -vvr1
                vv1 = np.array((vx1, vy1))
                vv2 = np.array((vx2, vy2))
                # nvvr = vv1 - 2 * np.vdot(pv1, vvr) * (pv1 / (np.vdot(pv1, pv1)))
                # a[i, 2:] = vvr / np.sqrt(np.vdot(vvr, vvr)) * 50
                # a[valid, 2:] = nvvr / np.sqrt(np.vdot(nvvr, nvvr)) * 50
                #
                # vv2 = np.array((vx2, vy2))
                #
                # pv1 = np.array(((x2 - x1), (y2 - y1)))
                # vv1 = np.array((vx1, vy1))
                # nvv1 = vv2 - 2 * np.vdot(pv1, vv1) * (pv1 / np.vdot(pv1, pv1))#*sqrt(np.vdot(vvr, vvr)/np.vdot(vv1, vv1))
                #
                # pv2 = np.array(((x1 - x2), (y1 - y2)))
                # nvv2 = vv1 - 2 * np.vdot(pv2, vv2) * (pv2 / np.vdot(pv2, pv2))# * sqrt(np.vdot(vvr, vvr)/np.vdot(vv2, vv2))
                #
                # a[valid, 2:] = nvv2 / sqrt(np.vdot(nvv2, nvv2)) * 50
                # a[i, 2:] = nvv1 / sqrt(np.vdot(nvv1, nvv1)) * 50

                a[i, 2:] = vvr1/2
                a[valid, 2:] = vvr2/2

    return a
