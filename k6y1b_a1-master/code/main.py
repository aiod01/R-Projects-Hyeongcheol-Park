# standard Python imports
import os
import argparse
import time
import pickle
import simple_decision

# 3rd party libraries
import numpy as np                              # this comes with Anaconda
import matplotlib.pyplot as plt                 # this comes with Anaconda
import pandas as pd                             # this comes with Anaconda
from sklearn.tree import DecisionTreeClassifier # see http://scikit-learn.org/stable/install.html
from sklearn.neighbors import KNeighborsClassifier # same as above

# CPSC 340 code
import utils
from decision_stump import DecisionStump, DecisionStumpEquality, DecisionStumpInfoGain
from decision_tree import DecisionTree
from knn import KNN, CNN

def load_dataset(filename):
    with open(os.path.join('..','data',filename), 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--question', required=True,
        choices=["1.1", "2", "2.2", "2.3", "2.4", "3", "3.1", "3.2", "4.1", "4.2", "5"])

    io_args = parser.parse_args()
    question = io_args.question

    if question == "1.1":
        
        fluTrends = pd.read_csv("../data/fluTrends.csv")
        fluTrends_array = fluTrends.values
        
        a = np.amax(fluTrends_array)
        b = np.amin(fluTrends_array)
        c = np.mean(fluTrends_array)
        d = np.median(fluTrends_array)
        e = utils.mode(fluTrends_array)
        
        print("maximum value of the dataset: ", a,
              "minimum value of the dataset: ", b,
              "mean of the dataset: ", c,
              "median of the dataset: ", d,
              "mode of the dataset: ", e)
        
        f = np.percentile(fluTrends_array, [5,25,50,75,95])
        
        print("5% quantile: ", f[0],
              "25% quantile: ", f[1],
              "50% quantile: ", f[2],
              "75% quantile: ", f[3],
              "95% quantile: ", f[4])
        
        mean = pd.DataFrame.mean(fluTrends, axis=0)
        var = pd.DataFrame.var(fluTrends, axis=0)
        
        g = mean.argmin()
        h = mean.argmax()
        i = var.argmin()
        j = var.argmax()
        
        print("The region with the minimum mean is: ", g,
              "The region with the maximum mean is: ", h,
              "The region with the minimum variance is: ", i,
              "The region with the maximum variance is: ", j)
        
        
    
    elif question == "2":

        # 1. Load citiesSmall dataset
        dataset = load_dataset("citiesSmall.pkl")
        X = dataset["X"]
        y = dataset["y"]

        # 2. Evaluate majority predictor model
        y_pred = np.zeros(y.size) + utils.mode(y)

        error = np.mean(y_pred != y)
        print("Mode predictor error: %.3f" % error)

        # 3. Evaluate decision stump
        model = DecisionStumpEquality()
        model.fit(X, y)
        y_pred = model.predict(X)

        error = np.mean(y_pred != y) 
        print("Decision Stump with inequality rule error: %.3f" % error)

        # PLOT RESULT
        utils.plotClassifier(model, X, y)

        fname = os.path.join("..", "figs", "q2_decisionBoundary.pdf")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)


    elif question == "2.2":
        # 1. Load citiesSmall dataset
        dataset = load_dataset("citiesSmall.pkl")
        X = dataset["X"]
        y = dataset["y"]

        # 3. Evaluate decision stump
        model = DecisionStump()
        model.fit(X, y)
        y_pred = model.predict(X)

        error = np.mean(y_pred != y)
        print("Decision Stump with inequality rule error: %.3f" % error)

        # PLOT RESULT
        utils.plotClassifier(model, X, y)

        fname = os.path.join("..", "figs", "q2_2_decisionBoundary.pdf")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)

    elif question == "2.3":
        # 1. Load citiesSmall dataset
        dataset = load_dataset("citiesSmall.pkl")
        X = dataset["X"]
        y = dataset["y"]

        # 2. Evaluate decision tree
        model = DecisionTree(max_depth=2)
        model.fit(X, y)

        y_pred = model.predict(X)
        error = np.mean(y_pred != y)

        print("Error: %.3f" % error)
        
        # 3. Printing Splitting Variables and Values
        print("Split Variable: ", model.splitModel.splitVariable)
        print("Split Value: ", model.splitModel.splitValue)
        print("SubModel1 Split Variable: ", model.subModel1.splitModel.splitVariable)
        print("SubModel1 Split Value: ", model.subModel1.splitModel.splitValue)
        print("SubModel0 Split Variable: ", model.subModel0.splitModel.splitVariable)
        print("SubModel0 Split Value: ", model.subModel0.splitModel.splitValue)
        print("SubModel1 Output: ", model.subModel1.splitModel.splitSat)
        print("SubModel0 Output: ", model.subModel0.splitModel.splitSat)
        
        
        # 4. Evaluate Simple Decision
        y_pred2 = simple_decision.simple_decision(X)
        error2 = np.mean(y_pred2 != y)
        print("Error from Simple Decision: %.3f" % error2)
        
        
        
    
    elif question == "2.4":
        dataset = load_dataset("citiesSmall.pkl")
        X = dataset["X"]
        y = dataset["y"]
        print("n = %d" % X.shape[0])

        depths = np.arange(1,15) # depths to try

        t = time.time()
        my_tree_errors = np.zeros(depths.size)
        for i, max_depth in enumerate(depths):
            model = DecisionTree(max_depth=max_depth)
            model.fit(X, y)
            y_pred = model.predict(X)
            my_tree_errors[i] = np.mean(y_pred != y)
        print("Our decision tree took %f seconds" % (time.time()-t))
        
        plt.plot(depths, my_tree_errors, label="mine")
        
        t = time.time()
        sklearn_tree_errors = np.zeros(depths.size)
        for i, max_depth in enumerate(depths):
            model = DecisionTreeClassifier(max_depth=max_depth, criterion='entropy', random_state=1)
            model.fit(X, y)
            y_pred = model.predict(X)
            my_tree_errors[i] = np.mean(y_pred != y)
        print("scikit-learn's decision tree took %f seconds" % (time.time()-t))

        
        plt.plot(depths, my_tree_errors, label="sklearn")
        plt.xlabel("Depth of tree")
        plt.ylabel("Classification error")
        plt.legend()
        fname = os.path.join("..", "figs", "q2_4_tree_errors.pdf")
        plt.savefig(fname)
        
        tree = DecisionTreeClassifier(max_depth=1)
        tree.fit(X, y)

        y_pred = tree.predict(X)
        error = np.mean(y_pred != y)

        print("Error: %.3f" % error)


    elif question == "3":
        dataset = load_dataset("citiesSmall.pkl")
        X, y = dataset["X"], dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"]        
        model = DecisionTreeClassifier(max_depth=2, criterion='entropy', random_state=1)
        model.fit(X, y)

        y_pred = model.predict(X)
        tr_error = np.mean(y_pred != y)

        y_pred = model.predict(X_test)
        te_error = np.mean(y_pred != y_test)
        print("Training error: %.3f" % tr_error)
        print("Testing error: %.3f" % te_error)

    elif question == "3.1":
        
        depths = np.arange(1,15)
        dataset = load_dataset("citiesSmall.pkl")
        X, y = dataset["X"], dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"]        
        
        
        my_training_errors = np.zeros(depths.size)
        my_testing_errors = np.zeros(depths.size)
        
        for i, max_depth in enumerate(depths):
            model = DecisionTreeClassifier(max_depth=max_depth, criterion='entropy', random_state=1)
            model.fit(X, y)
            y_pred = model.predict(X)
            my_training_errors[i] = np.mean(y_pred != y)
            y_pred_test = model.predict(X_test)
            my_testing_errors[i] = np.mean(y_pred_test != y_test)
            
        plt.plot(depths, my_training_errors, label="training_errors")
        plt.plot(depths, my_testing_errors, label="testing_errors")
        
        plt.xlabel("Depth of tree")
        plt.ylabel("Classification error")
        plt.legend()
        fname = os.path.join("..", "figs", "q3_1_tree_errors.pdf")
        plt.savefig(fname)
        
        
        
    elif question == "3.2":
        
        depths = np.arange(1,15)
        dataset = load_dataset("citiesSmall.pkl")
        X, y = dataset["X"], dataset["y"]
        X_training, X_val = X[:200,:], X[200:,:]
        y_training, y_val = y[:200], y[200:]
        
        errors1 = np.zeros(depths.size)
        errors2 = np.zeros(depths.size)
        
        for i, max_depth in enumerate(depths):
            model = DecisionTreeClassifier(max_depth=max_depth, criterion='entropy', random_state=1)
            model.fit(X_training, y_training)
            y_pred_test = model.predict(X_val)
            errors1[i] = np.mean(y_pred_test != y_val)
            
        for i, max_depth in enumerate(depths):
            model = DecisionTreeClassifier(max_depth=max_depth, criterion='entropy', random_state=1)
            model.fit(X_val, y_val)
            y_pred_training = model.predict(X_training)
            errors2[i] = np.mean(y_pred_training != y_training)
            
        plt.plot(depths, errors1)
        plt.plot(depths, errors2)
        
        plt.xlabel("Depth of tree")
        plt.ylabel("Classification error")
        plt.legend()
        fname = os.path.join("..", "figs", "q3_2_tree_errors.pdf")
        plt.savefig(fname)
        

    if question == '4.1':
        
        dataset = load_dataset("citiesSmall.pkl")
        X = dataset["X"]
        y = dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"] 

        model = KNN(1)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        y_pred2 = model.predict(X)

        error = np.mean(y_pred != y_test) 
        error2 = np.mean(y_pred2 != y)
        print("KNN test error k=1: %.3f" % error)
        
        print("KNN training error k=1: %.3f" % error2)

        # PLOT RESULT
        utils.plotClassifier(model, X, y)

        fname = os.path.join("..", "figs", "q4_1_k1_KNN.pdf")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)
        
        
        
        model = KNeighborsClassifier(1)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        y_pred2 = model.predict(X)

        error = np.mean(y_pred != y_test) 
        error2 = np.mean(y_pred2 != y)
        print("KNClassifier test error k=1: %.3f" % error)
        
        print("KNClassifier training error k=1: %.3f" % error2)

        # PLOT RESULT
        utils.plotClassifier(model, X, y)

        fname = os.path.join("..", "figs", "q4_1_k1_KNClassifier.pdf")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)
        
        
        
        model = KNN(3)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        y_pred2 = model.predict(X)

        error = np.mean(y_pred != y_test) 
        error2 = np.mean(y_pred2 != y)
        print("KNN test error k=3: %.3f" % error)
        print("KNN training error k=3: %.3f" % error2)



        
        model = KNN(10)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        y_pred2 = model.predict(X)

        error = np.mean(y_pred != y_test)
        error2 = np.mean(y_pred2 != y)
        print("KNN test error k=10: %.3f" % error)
        print("KNN training error k=10: %.3f" % error2)


    if question == '4.2':
        
        t1 = time.time()
        dataset = load_dataset("citiesBig1.pkl")
        X = dataset["X"]
        y = dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"]
        model = CNN(1)
        model.fit(X, y)
        model.predict(X)
        print("CNN took %f seconds" % (time.time()-t1))
        
        t2 = time.time()
        dataset = load_dataset("citiesBig1.pkl")
        X = dataset["X"]
        y = dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"]
        model = KNN(1)
        model.fit(X, y)
        model.predict(X)
        print("KNN took %f seconds" % (time.time()-t2))

        
        
        model = CNN(1)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        y_pred2 = model.predict(X)

        error = np.mean(y_pred != y_test) 
        error2 = np.mean(y_pred2 != y)
        print("CNN test error k=1 citiesBig1: %.3f" % error)
        print("CNN training error k=1 citiesBig1: %.3f" % error2)
        print("There are %.3f variables" % model.num)
        
        
        # PLOT RESULT
        utils.plotClassifier(model, X, y)

        fname = os.path.join("..", "figs", "q4_2_CNN.pdf")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)
        
        
        
        dataset = load_dataset("citiesBig2.pkl")
        X = dataset["X"]
        y = dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"]
        
        model = CNN(1)
        model.fit(X, y)
        y_pred = model.predict(X_test)
        y_pred2 = model.predict(X)

        error = np.mean(y_pred != y_test) 
        error2 = np.mean(y_pred2 != y)
        print("CNN test error k=1 citiesBig2: %.3f" % error)
        print("CNN training error k=1 citiesBig2: %.3f" % error2)
        
        
        
        t = time.time()
        dataset = load_dataset("citiesBig1.pkl")
        X = dataset["X"]
        y = dataset["y"]
        X_test, y_test = dataset["Xtest"], dataset["ytest"]
                
        model2 = DecisionTreeClassifier()
        model2.fit(X, y)

        y_pred = model2.predict(X)
        tr_error = np.mean(y_pred != y)

        y_pred_test = model2.predict(X_test)
        te_error = np.mean(y_pred_test != y_test)
        print("Decision Tree Training error citiesBig1: %.3f" % tr_error)
        print("Decision Tree Testing error citiesBig1: %.3f" % te_error)
        print("Decision Tree took %f seconds" % (time.time()-t))
        
        utils.plotClassifier(model2, X, y)

        fname = os.path.join("..", "figs", "q4_2_DT.pdf")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)

