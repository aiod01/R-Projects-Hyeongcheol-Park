"""
Implementation of k-nearest neighbours classifier
"""

import numpy as np
from scipy import stats
import utils

class KNN:

    def __init__(self, k):
        self.k = k

    def fit(self, X, y):
        self.X = X # just memorize the trianing data
        self.y = y 

    def predict(self, Xtest):
        
        dist = utils.euclidean_dist_squared(self.X, Xtest)
        yhat = np.zeros(len(Xtest))
        for i in range(0, len(Xtest)):
            nearest = np.argsort(dist[:,i])
            yhat[i] = utils.mode(self.y[nearest[:self.k]])
        return yhat
            
        
        


class CNN(KNN):

    def fit(self, X, y):
        """
        Parameters
        ----------
        X : an N by D numpy array
        y : an N by 1 numpy array of integers in {1,2,3,...,c}
        """

        Xcondensed = X[0:1,:]
        ycondensed = y[0:1]
        
        num = 1

        for i in range(1,len(X)):
            x_i = X[i:i+1,:]
            dist2 = utils.euclidean_dist_squared(Xcondensed, x_i)
            inds = np.argsort(dist2[:,0])
            yhat = utils.mode(ycondensed[inds[:min(self.k,len(Xcondensed))]])

            if yhat != y[i]:
                Xcondensed = np.append(Xcondensed, x_i, 0)
                ycondensed = np.append(ycondensed, y[i])
                num = num + 1

        self.X = Xcondensed
        self.y = ycondensed
        self.num = num