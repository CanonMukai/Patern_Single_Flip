# -*- coding:utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt

L = 3
N = L*L
ND = 20
T_LOOP = 1000
S_LOOP = 1000
O_LOOP = 10


stat = np.random.randint(0, 2, N)
stat_memo = stat
stat = 2*stat - 1
stat_int = np.arra(stat)



def single_flip(beta):
    for i in range(N):
        ix = i % L
        iy = i / L
        de = 0.0

        if ix != 0:
            de += stat[(ix-1) + iy*L]
        else:
            de += stat[(L-1) + iy*L]
        if iy != 0:
            de += stat[ix + (iy-1)*L]
        else:
            de += stat[ix + (L-1)*L]

        if ix != L-1:
            de += stat[(ix+1) + iy*L]
        else:
            de += stat[0 + iy*L]
        if iy != L-1:
            de += stat[ix + (iy+1)*L]
        else:
            de += stat[ix + 0*L]

        de = de * 2.0 * stat[ix + iy*L]

        
        if de < 0 and math.exp(-beta * de) > np.random.rand():
            stat[i] = -stat[i]
            
def mc_onestep(beta):
    single_flip(beta)


def energy():
    e = 0.0
    for ix in range(L):
        for iy in range(L):
            s = stat[ix + iy*L]
            if ix != L-1:
                e -= s * stat[ix + 1 + iy*L]
            else:
                e -= s * stat[0 + iy*L]
            if iy != L-1:
                e -= s * stat[ix + (iy + 1)*L]
            else:
                e -= s * stat[ix + 0*L]
    e /= float(N)
    return e

def domc():
    bs = 0.3
    be = 0.6
    for i in range(ND):
        beta = bs + (be - bs) * float(i) / float(ND)
        for j in range(T_LOOP)
