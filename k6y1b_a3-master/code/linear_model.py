import numpy as np
from numpy.linalg import solve
from findMin import findMin
from scipy.optimize import approx_fprime
import utils

# Ordinary Least Squares
class LeastSquares:
    def fit(self,X,y):
        self.w = solve(X.T@X, X.T@y)

    def predict(self, X):
        return X@self.w

# Least squares where each sample point X has a weight associated with it.
class WeightedLeastSquares(LeastSquares): # inherits the predict() function from LeastSquares
    def fit(self,X,y,Z):
        self.w=solve(X.T@Z@X,X.T@Z@y)
    
    def predict(self, X):
        return X@self.w

class LinearModelGradient(LeastSquares):

    def fit(self,X,y):
        n, d = X.shape

        # Initial guess
        self.w = np.zeros((d, 1))

        # check the gradient
        estimated_gradient = approx_fprime(self.w, lambda w: self.funObj(w,X,y)[0], epsilon=1e-6)
        implemented_gradient = self.funObj(self.w,X,y)[1]
        if np.max(np.abs(estimated_gradient - implemented_gradient) > 1e-4):
            print('User and numerical derivatives differ: %s vs. %s' % (estimated_gradient, implemented_gradient));
        else:
            print('User and numerical derivatives agree.')

        self.w, f = findMin(self.funObj, self.w, 100, X, y)

    def funObj(self,w,X,y):
   
        pwr=X*w-y
        r=np.exp(pwr)+np.exp(-pwr)
        f=np.sum(np.log(r))
        #f = 0.5*np.sum((X@w - y)**2)

        # Calculate the gradient value
        #g = X.T@(X@w-y)
        num=np.exp(pwr)-np.exp(-pwr)
        denom=np.exp(pwr)+np.exp(-pwr)
        g=np.dot(X.T,(num/denom))
        
        return (f,g)


# Least Squares with a bias added
class LeastSquaresBias:

    def fit(self,X,y):
        n,m = X.shape
        X0 = np.ones((n,1))
        X = np.hstack((X0,X))
        self.w = solve(X.T@X, X.T@y)

    def predict(self, X):
        n,m = X.shape 
        X0 = np.ones((n,1))
        X = np.hstack((X0,X))
        return X@self.w

# Least Squares with polynomial basis
class LeastSquaresPoly:
    def __init__(self, p):
        self.leastSquares = LeastSquares()
        self.p = p

    def fit(self,X,y):
        Z=self.__polyBasis(X)
        self.w = solve(Z.T@Z, Z.T@y)
        

    def predict(self, X):
        Z=self.__polyBasis(X)
        return Z@self.w

    def __polyBasis(self, X):
        p=self.p
        n=X.shape[0]
        d=p+1
        Z=np.zeros((n,d))
        for i in range(d):
            X_col=X**i
            Z[:,i:i+1]=X_col
        
        return Z

# Least Squares with RBF Kernel
class LeastSquaresRBF:
    def __init__(self, sigma):
        self.sigma = sigma

    def fit(self,X,y):
        self.X = X
        n, d = X.shape

        Z = self.__rbfBasis(X, X, self.sigma)

        # Solve least squares problem
        a = Z.T@Z + 1e-12*np.identity(n) # tiny bit of regularization
        b = Z.T@y
        self.w = solve(a,b)

    def predict(self, Xtest):
        Z = self.__rbfBasis(Xtest, self.X, self.sigma)
        yhat = Z@self.w
        return yhat

    def __rbfBasis(self, X1, X2, sigma):
        n1 = X1.shape[0]
        n2 = X2.shape[0]
        d = X1.shape[1]
        den = 1 / np.sqrt(2 * np.pi * (sigma** 2))

        D = (X1**2)@np.ones((d, n2)) + \
            np.ones((n1, d))@(X2.T** 2) - \
            2 * (X1@X2.T)

        Z = den * np.exp(-1* D / (2 * (sigma**2)))
        return Z
