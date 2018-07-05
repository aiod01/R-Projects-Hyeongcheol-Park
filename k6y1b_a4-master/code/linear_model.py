import numpy as np
from numpy.linalg import solve
import findMin
from scipy.optimize import approx_fprime
import utils


class logReg:
    # Logistic Regression
    def __init__(self, verbose=0, maxEvals=100):
        self.verbose = verbose
        self.maxEvals = maxEvals
        self.bias = True

    def funObj(self, w, X, y):
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw)))

        # Calculate the gradient value
        res = - y / (1. + np.exp(yXw))
        g = X.T.dot(res)

        return f, g

    def fit(self,X, y):
        n, d = X.shape

        # Initial guess
        self.w = np.zeros(d)
        utils.check_gradient(self, X, y)
        (self.w, f) = findMin.findMin(self.funObj, self.w,
                                      self.maxEvals, X, y, verbose=self.verbose)
    def predict(self, X):
        return np.sign(X@self.w)

class logRegL1:
    # Logistic Regression
    def __init__(self, verbose=2, maxEvals=100, lammy=1):
        self.verbose = verbose
        self.maxEvals = maxEvals
        self.bias = True
        self.lammy=lammy

    def funObj(self, w, X, y):
        yXw = y * X.dot(w)
        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw)))

        # Calculate the gradient value

        res = - y / (1. + np.exp(yXw))
        g = X.T.dot(res)

        return f, g

    def fit(self,X, y):
        n, d = X.shape

        # Initial guess
        self.w = np.zeros(d)
        utils.check_gradient(self, X, y)
       
        (self.w, f) = findMin.findMinL1(self.funObj, self.w,
                                         self.lammy,
                                         self.maxEvals,X, y, 
                                         verbose=self.verbose
                                         )
    def predict(self, X):
        return np.sign(X@self.w)

class logRegL2:
    # Logistic Regression
    def __init__(self, verbose=2, maxEvals=100, lammy=1):
        self.verbose = verbose
        self.maxEvals = maxEvals
        self.bias = True
        self.lammy=lammy

    def funObj(self, w, X, y):
        lammy=self.lammy
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw))) + (lammy/2)*np.sum(w**2)

        # Calculate the gradient value
        res = -y / (1. + np.exp(yXw))
        g = X.T.dot(res)+ lammy*w

        return f, g

    def fit(self,X, y):
        n, d = X.shape

        # Initial guess
        self.w = np.zeros(d)
        utils.check_gradient(self, X, y)
        (self.w, f) = findMin.findMin(self.funObj, self.w,
                                      self.maxEvals, X, y, verbose=self.verbose)
    def predict(self, X):
        return np.sign(X@self.w)


class logRegL0(logReg):
    # L0 Regularized Logistic Regression
    def __init__(self, L0_lambda=1.0, verbose=2, maxEvals=400):
        self.verbose = verbose
        self.L0_lambda = L0_lambda
        self.maxEvals = maxEvals

    def fit(self, X, y):
        n, d = X.shape
        minimize = lambda ind: findMin.findMin(self.funObj,
                                                  np.zeros(len(ind)),
                                                  self.maxEvals,
                                                  X[:, ind], y, verbose=0)
        selected = set()
        selected.add(0)
        minLoss = np.inf
        oldLoss = 0
        bestFeature = -1

        while minLoss != oldLoss:
            oldLoss = minLoss
            print("Epoch %d " % len(selected))
            print("Selected feature: %d" % (bestFeature))
            print("Min Loss: %.3f\n" % minLoss)

            for i in range(d):
                if i in selected:
                    continue

                selected_new = selected | {i}
                # TODO for Q2.3: Fit the model with 'i' added to the features,
                # then compute the loss and update the minLoss/bestFeature
                w,_ = minimize(list(selected_new))
                yXw = y*X[:,list(selected_new)].dot(w)
                #calculate new logistic loss
                loss = np.sum(np.log(1. + np.exp(-yXw))) + self.L0_lambda * np.count_nonzero(w)
                if loss < minLoss:
                    minLoss = loss
                    bestFeature = i

            selected.add(bestFeature)

        self.w = np.zeros(d)
        self.w[list(selected)], _ = minimize(list(selected))


class leastSquaresClassifier:
    def fit(self, X, y):
        n, d = X.shape
        self.n_classes = np.unique(y).size

        # Initial guess
        self.W = np.zeros((self.n_classes,d))

        for i in range(self.n_classes):
            ytmp = y.copy().astype(float)
            ytmp[y==i] = 1
            ytmp[y!=i] = -1

            # solve the normal equations
            # with a bit of regularization for numerical reasons
            self.W[i] = np.linalg.solve(X.T@X+0.0001*np.eye(d), X.T@ytmp)

    def predict(self, X):
        return np.argmax(X@self.W.T, axis=1)
    

        return np.argmax(X@self.W.T, axis=1)
    
class logLinearClassifier:
    def __init__(self, verbose=2, maxEvals=400):
        self.verbose = verbose
        self.maxEvals = maxEvals
    
    def funObj(self, w, X, y):
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw)))

        # Calculate the gradient value
        res = - y / (1. + np.exp(yXw))
        g = X.T.dot(res)

        return f, g

    def fit(self, X, y):
        n, d = X.shape    
        self.n_classes = np.unique(y).size
        

        # Initial guess
        self.W = np.zeros((d, self.n_classes))
        
        for i in range(self.n_classes):
            ytmp = y.copy().astype(float)
            ytmp[y==i] = 1
            ytmp[y!=i] = -1

            self.W[:, i],_ = findMin.findMin(self.funObj, self.W[:,i],self.maxEvals,X,ytmp, verbose=self.verbose)

    def predict(self, X):
        yhat = np.dot(X, self.W)

        return np.argmax(yhat, axis=1)

class softmaxClassifier:
    def __init__(self, verbose=1, maxEvals=400):
        self.verbose = verbose
        self.maxEvals = maxEvals
    
    def funObj(self, w, X, y):
        n, d = X.shape
        n_classes = self.n_classes
        
        #reshape w into d x k matrix
        w = w.reshape(d,n_classes)
        
        #calculate Xw and normalizing constant
        Xw = X.dot(w)
        nc = np.sum(np.exp(Xw),1)
        
        #Calculate Xw with the y-th column of w
        Xw_i = np.zeros(n)
        for i  in range(n):
            Xw_i[i] = X[i,:].dot(w[:,y[i]])


        # Calculate the function value
        f = np.sum(-Xw_i + np.log(nc))

        # Calculate the gradient value
        g = np.zeros((d,n_classes))
        for i in range(n_classes):
            g[:,i] = np.transpose(X).dot(np.exp(Xw[:,i])/nc - (y==i))
        #g = np.transpose(g.reshape(n_classes*d,))

        return f, g.ravel()

    def fit(self, X, y):
        n, d = X.shape    
        self.n_classes = np.unique(y).size

        # Initial guess
        self.W = np.zeros(d*self.n_classes)
        self.W = findMin.findMin(self.funObj, self.W,self.maxEvals,X,y,verbose=self.verbose)

    def predict(self, X):
        w = self.W[0]
        n, d = X.shape
        n_classes = self.n_classes
        w = w.reshape(d,n_classes)
        yhat = np.dot(X,w)

        return np.argmax(yhat, axis=1)