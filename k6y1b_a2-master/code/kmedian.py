import numpy as np
import utils 

class Kmedian:

    def __init__(self, k):
        self.k = k

    def fit(self, X):
        N, D = X.shape
        y = np.ones(N)

        median = np.zeros((self.k, D))
        for kk in range(self.k):
            i = np.random.randint(N)
            median[kk] = X[i]#이게 행렬일 때 하나만 하면 행을 먹는구나.

        while True:
            y_old = y

            # Compute euclidean distance to each mean
            dist1 = utils.manhattan_dist(X, median)
            dist1[np.isnan(dist1)] = np.inf
            y = np.argmin(dist1, axis=1)
            error=np.sum(np.min(dist1, axis=1))
#            print("The error is ",error)
            # Update means
            for kk in range(self.k):
                median[kk] = np.median(X[y==kk],axis=0)

            changes = np.sum(y != y_old)
            # print('Running K-means, changes in cluster assignment = {}'.format(changes))

            # Stop if no point changed cluster
            if changes == 0:
                break

        self.median = median

    def predict(self, X):
        median = self.median
        dist1 = utils.manhattan_dist(X, median)
        dist1[np.isnan(dist1)] = np.inf
        return np.argmin(dist1, axis=1)
    
    def error(self, X): 
        median=self.median
        dist1 = utils.manhattan_dist(X, median)
        dist1[np.isnan(dist1)] = np.inf
        error=np.sum(np.min(dist1, axis=1))
        return error
