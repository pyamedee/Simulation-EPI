# -*- coding:Utf-8 -*-

import numpy as np
cimport numpy as np

import cython
cimport cython

cdef np.ndarray get_distances(np.ndarray array, np.ndarray coords):
    cdef np.ndarray a = array - coords
    a **= 2
    return np.sqrt(a[:, 0] + a[:, 1])


cdef set get_collisions(np.ndarray a, int collision_distance):

    cdef pairs set = set()
    cdef keys set = set()  # contains already paired positions
    cdef position ndarray
    cdef distances ndarray
    cdef valids tuple
    cdef pair frozenset
    for i in range(a.shape[0]):
        if i not in keys:
            position = a[i]
            distances = get_distances(a, position)
            valids = (distances < collision_distance).nonzero()[0]
            for valid in (v for v in valids if v != i):
                pair = frozenset((i, valid))
                pairs.add(pair)
                keys.add(valid)
    return pairs
