from random_tree import RandomTree
import numpy as np
import utils

class RandomForest:
    def __init__(self, max_depth,num_trees):
        model=[]
        
        for i in range(num_trees):
            #Add random Tree model to model list
            model.append(RandomTree(max_depth=max_depth))
        
        self.num_trees=num_trees
        self.model=model
        

    def fit(self,X,y):
        num_trees=self.num_trees
        model=self.model
        trees=[]

        #Fit random tree
        for i in range(num_trees):
            #Add fitted Random Tree model to tree list
            trees.append(model[i].fit(X,y))

        # Save random num_trees
        self.trees=trees

    def predict(self, X):
        num_trees=self.num_trees
        model=self.model
        N,D = X.shape
        y_pred=np.zeros((num_trees,N))
        for i in range(num_trees):
                #model[i].fit(x,y)
                #make predicitons based on each random tree
                y_pred[i, :]=model[i].predict(X)

        yhat=np.zeros(N)
        for n in range(N):
            #Select the model among allp predicted values as our final decision_tree
            yhat[n]=utils.mode(y_pred[:,n])

        return yhat
