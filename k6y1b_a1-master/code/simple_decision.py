#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np

def simple_decision(X):

    N, D = X.shape
    y = np.zeros(N)

    for i in range(N):

        if X[i,1] > 37.669007:

               if X[i,0] > -96.090109:

                         y[i] = 0

               else:

                         y[i] = 1


        else:

               if X[i,0] > -115.577574:

                         y[i] = 1

               else:

                         y[i] = 0
    return y
