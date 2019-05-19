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


cdef np.ndarray get_distances(np.ndarray arr, np.ndarray coords):
    cdef np.ndarray a = np.abs(arr - coords) ** 2
    return a[:, 0] + a[:, 1]


cpdef dict calculate_new_vectors(np.ndarray a, int collision_distance,
                                 int squared_collision_distance):
    cdef dict pairs = {}
    cdef np.ndarray position
    cdef np.ndarray squared_distances
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
    
    cdef np.ndarray pv1
    cdef np.ndarray npv1
    
    cdef np.ndarray pv2
    cdef np.ndarray npv2
    
    cdef tuple tp1
    cdef tuple tp2
    
    cdef np.ndarray vv1
    cdef np.ndarray vv2
    
    cdef np.ndarray a1
    cdef np.ndarray a2
    
    cdef np.ndarray d1
    cdef np.ndarray av1
    cdef np.ndarray arr1
    
    cdef np.ndarray d2
    cdef np.ndarray av2
    cdef np.ndarray arr2
    
    cdef np.ndarray contact_point
    
    cdef np.ndarray adcav1
    cdef float dcav1
    
    cdef np.ndarray adcarr1
    cdef float dcarr1
    
    cdef np.ndarray adcav2
    cdef float dcav2
    
    cdef np.ndarray adcarr2
    cdef float dcarr2
    
    cdef np.ndarray nvv1
    cdef np.ndarray nvv2
    
    for i in range(a.shape[0]):
        position = a[i, :2]
        squared_distances = get_distances(a[:, :2], position)
        valids = (squared_distances < squared_collision_distance).nonzero()[0]
        for valid in valids:
            if pairs.get(i, None) is None and valid != i:
                pairs[valid] = i
                x1, y1, vx1, vy1 = a[i]
                x2, y2, vx2, vy2 = a[valid]

                pv1 = np.array(((x2 - x1), (y2 - y1)))
                npv1 = np.dot(pv1, pv1)
                pv1 = pv1 / sqrt(npv1) * collision_distance

                pv2 = np.array(((x1 - x2), (y1 - y2)))
                npv2 = np.dot(pv2, pv2)
                pv2 = pv2 / sqrt(npv2) * collision_distance

                tp1 = x1, y1
                tp2 = x2, y2
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

                    a[valid, :] = x2, y2, *nvv2 / sqrt(np.dot(nvv2, nvv2)) * 50
                    a[i, :] = x1, y1, *nvv1 / sqrt(np.dot(nvv1, nvv1)) * 50

                else:
                    a[valid, :] = x2, y2, vx1, vy1
                    a[i, :] = x1, y1, vx2, vy2

                # print(sqrt(np.dot(pv1, pv1)), sqrt(np.dot(pv2, pv2)))

                # a[i, 2:] = vvr1/2
                # a[valid, 2:] = vvr2/2

    return pairs


