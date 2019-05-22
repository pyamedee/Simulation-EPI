# -*- coding: utf-8 -*-
"""
Created on Sun May 19 14:16:10 2019

@author: Hélène Le Berre
"""

import numpy as np
cimport numpy as np

import cython
cimport cython

from math import sqrt

DTYPE = np.float
ctypedef np.float_t DTYPE_t

DTYPE_INT = np.int
ctypedef np.int_t DTYPE_INT_t

cdef np.ndarray get_distances(np.ndarray[DTYPE_t, ndim=2] arr, np.ndarray[DTYPE_t] coords):
    cdef np.ndarray a = np.abs(arr - coords) ** 2
    return a[:, 0] + a[:, 1]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dict calculate_new_vectors(np.ndarray[DTYPE_t, ndim=2] a, int collision_distance,
                                 int squared_collision_distance, np.ndarray enabled_entities):
    cdef dict pairs = {}
    cdef np.ndarray[DTYPE_t] position
    cdef np.ndarray[DTYPE_t] squared_distances
    cdef np.ndarray valids
    cdef int valid
    cdef int i
    
    cdef float x1
    cdef float y1
    cdef float vx1
    cdef float vy1
    
    cdef float x2
    cdef float y2
    cdef float vx2
    cdef float vy2
    
    cdef np.ndarray[DTYPE_t] pv1
    cdef float npv1
    
    cdef np.ndarray[DTYPE_t] pv2
    cdef float npv2
    
    cdef np.ndarray[DTYPE_t] tp1
    cdef np.ndarray[DTYPE_t] tp2
    
    cdef np.ndarray[DTYPE_t] vv1
    cdef np.ndarray[DTYPE_t] vv2
    
    cdef np.ndarray[DTYPE_t] a1
    cdef np.ndarray[DTYPE_t] a2
    
    cdef np.ndarray[DTYPE_t] d1
    cdef np.ndarray[DTYPE_t] av1
    cdef np.ndarray[DTYPE_t] arr1
    
    cdef np.ndarray[DTYPE_t] d2
    cdef np.ndarray[DTYPE_t] av2
    cdef np.ndarray[DTYPE_t] arr2
    
    cdef np.ndarray[DTYPE_t] contact_point
    
    cdef np.ndarray[DTYPE_t] adcav1
    cdef float dcav1
    
    cdef np.ndarray[DTYPE_t] adcarr1
    cdef float dcarr1
    
    cdef np.ndarray[DTYPE_t] adcav2
    cdef float dcav2
    
    cdef np.ndarray[DTYPE_t] adcarr2
    cdef float dcarr2
    
    cdef np.ndarray[DTYPE_t] nvv1
    cdef np.ndarray[DTYPE_t] nvv2

    cdef np.ndarray[DTYPE_t, ndim=2] earr = a[:, :2]

    for i in range(a.shape[0]):
        if enabled_entities[i]:
            position = a[i, :2]
            squared_distances = get_distances(earr, position)
            valids = (squared_distances < squared_collision_distance).nonzero()[0]
            for valid in valids:
                if enabled_entities[valid] and pairs.get(i, None) is None and valid != i:
                    pairs[valid] = i
                    x1, y1, vx1, vy1 = a[i]
                    x2, y2, vx2, vy2 = a[valid]

                    pv1 = np.array(((x2 - x1), (y2 - y1)))
                    npv1 = np.dot(pv1, pv1)
                    pv1 = pv1 / sqrt(npv1) * collision_distance

                    pv2 = np.array(((x1 - x2), (y1 - y2)))
                    npv2 = np.dot(pv2, pv2)
                    pv2 = pv2 / sqrt(npv2) * collision_distance

                    tp1 = np.array((x1, y1))
                    tp2 = np.array((x2, y2))
                    x2, y2 = pv1 + tp1
                    x1, y1 = pv2 + tp2

                    # vvr = np.abs(np.array((vx2 - vx1, vy2 - vy1)))
                    # vvr2 = -vvr1
                    vv1 = np.array((vx1, vy1))
                    vv2 = np.array((vx2, vy2))
                    # nvvr = vv1 - 2 * np.dot(pv1, vvr) * (pv1 / (np.dot(pv1, pv1)))
                    # a[i, 2:] = vvr / np.sqrt(np.dot(vvr, vvr)) * 50
                    # a[valid, 2:] = nvvr / np.sqrt(np.dot(nvvr, nvvr)) * 50

                    # vv2 = np.array((vx2, vy2))

                    # pv1 = np.array(((x2 - x1), (y2 - y1)))
                    # vv1 = np.array((vx1, vy1))

                    a1 = np.array((x1, y1))
                    a2 = np.array((x2, y2))

                    d1 = vv1 / 50 * (collision_distance / 2)
                    av1 = d1 + a1
                    arr1 = a1 - d1

                    d2 = vv2 / 50 * (collision_distance / 2)
                    av2 = d2 + a2
                    arr2 = a2 - d2

                    contact_point = (a1 + a2) / 2

                    adcav1 = (av1 - contact_point) ** 2
                    dcav1 = sqrt(adcav1[0] + adcav1[1])

                    adcarr1 = (arr1 - contact_point) ** 2
                    dcarr1 = sqrt(adcarr1[0] + adcarr1[1])

                    adcav2 = (av2 - contact_point) ** 2
                    dcav2 = sqrt(adcav2[0] + adcav2[1])

                    adcarr2 = (arr2 - contact_point) ** 2
                    dcarr2 = sqrt(adcarr2[0] + adcarr2[1])

                    if dcav1 < dcarr1 and dcav2 < dcarr2:

                        nvv1 = vv1 - 2 * np.dot(pv1, vv1) * (pv1 / npv1)  # * sqrt(np.dot(vvr, vvr)/np.dot(vv1, vv1))
                        nvv2 = vv2 - 2 * np.dot(pv2, vv2) * (pv2 / npv2)  # * sqrt(np.dot(vvr, vvr)/np.dot(vv2, vv2))

                        a[valid, :2] = x2, y2
                        a[valid, 2:] = nvv2 / sqrt(np.dot(nvv2, nvv2)) * 50
                        a[i, :2] = x1, y1
                        a[i, 2:] = nvv1 / sqrt(np.dot(nvv1, nvv1)) * 50

                    else:
                        a[valid, :] = x2, y2, vx1, vy1
                        a[i, :] = x1, y1, vx2, vy2

                    # print(sqrt(np.dot(pv1, pv1)), sqrt(np.dot(pv2, pv2)))

                    # a[i, 2:] = vvr1/2
                    # a[valid, 2:] = vvr2/2

    return pairs


