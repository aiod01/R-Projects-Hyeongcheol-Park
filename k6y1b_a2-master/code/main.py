# basics
import os
import pickle
import argparse
import matplotlib.pyplot as plt
import numpy as np
import time


# sklearn imports
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from skimage.io import imread, imshow, imsave


# our code
from naive_bayes import NaiveBayes

from decision_stump import DecisionStump, DecisionStumpEquality, DecisionStumpInfoGain
from decision_tree import DecisionTree
from random_tree import RandomTree
from random_forest import RandomForest


from kmeans import Kmeans
from kmedian import Kmedian
from quantize_image import ImageQuantizer
from sklearn.cluster import DBSCAN

def plot_2dclustering(X,y):
    plt.scatter(X[:,0], X[:,1], c=y)
    plt.title('Cluster Plot')


def load_dataset(filename):
    with open(os.path.join('..','data',filename), 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--question', required=True)

    io_args = parser.parse_args()
    question = io_args.question

    if question == '1.2':
        dataset = load_dataset("newsgroups.pkl")

        X = dataset["X"]
        y = dataset["y"]
        X_valid = dataset["Xvalidate"]
        y_valid = dataset["yvalidate"]
        groupnames = dataset["groupnames"]
        wordlist = dataset["wordlist"]

        print("colum 50 is ",wordlist[50])
        print("The words are", wordlist[np.where(X[500,])])
        print("The group name is",groupnames[y[500]])

    elif question == '1.3':
        dataset = load_dataset("newsgroups.pkl")

        X = dataset["X"]
        y = dataset["y"]
        X_valid = dataset["Xvalidate"]
        y_valid = dataset["yvalidate"]

        print("d = %d" % X.shape[1])
        print("n = %d" % X.shape[0])
        print("t = %d" % X_valid.shape[0])
        print("Num classes = %d" % len(np.unique(y)))

        model = RandomForestClassifier()
        model.fit(X, y)
        y_pred = model.predict(X_valid)
        v_error = np.mean(y_pred != y_valid)
        print("Random Forest (sklearn) validation error: %.3f" % v_error)

        model = NaiveBayes(num_classes=4)
        model.fit(X, y)
        y_pred = model.predict(X_valid)
        v_error = np.mean(y_pred != y_valid)
        print("Naive Bayes (ours) validation error: %.3f" % v_error)

        model = BernoulliNB()
        model.fit(X, y)
        y_pred = model.predict(X_valid)
        v_error = np.mean(y_pred != y_valid)
        print("Naive Bayes (sklearn) validation error: %.3f" % v_error)

    elif question == '2':
        dataset = load_dataset('vowel.pkl')
        X = dataset['X']
        y = dataset['y']
        X_test = dataset['Xtest']
        y_test = dataset['ytest']
        print("\nn = %d, d = %d\n" % X.shape)

        def evaluate_model(model):
            model.fit(X,y)

            y_pred = model.predict(X)
            tr_error = np.mean(y_pred != y)

            y_pred = model.predict(X_test)
            te_error = np.mean(y_pred != y_test)
            print("    Training error: %.3f" % tr_error)
            print("    Testing error: %.3f" % te_error)


#        print("Our implementations:")
#        print("  Decision tree info gain")
#        evaluate_model(DecisionTree(max_depth=np.inf, stump_class=DecisionStumpInfoGain))
#        print("  Random tree info gain")
#        evaluate_model(RandomTree(max_depth=np.inf))
        print("  Random forest info gain")
        t=time.time()
        evaluate_model(RandomForest(max_depth=np.inf, num_trees=50))
        print("My random forst took %f seconds" % (time.time()-t))

#        print("sklearn implementations")
#        print("  Decision tree info gain")
#        evaluate_model(DecisionTreeClassifier(criterion="entropy"))
#        print("  Random forest info gain")
#        evaluate_model(RandomForestClassifier(criterion="entropy"))
        print("  Random forest info gain, more trees")
        t=time.time()
        evaluate_model(RandomForestClassifier(criterion="entropy", n_estimators=50))
        print("sikit learn random forst took %f seconds" % (time.time()-t))

        

    elif question == '3':
        X = load_dataset('clusterData.pkl')['X']

        model = Kmeans(k=4)
        model.fit(X)
        plot_2dclustering(X, model.predict(X))

        fname = os.path.join("..", "figs", "kmeans_basic.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)

    elif question == '3.1':
        X = load_dataset('clusterData.pkl')['X']
        model_list=[]
        error_np=np.zeros(50)
        for i in range(50):
            model=Kmeans(k=4)
            model.fit(X)
            model_list.append(model)
            error_np[i]=model.error(X)
        final_model=model_list[np.argmin(error_np)]
        plot_2dclustering(X,final_model.predict(X))
        fname = os.path.join("..", "figs", "by_chopa.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)
        

    elif question == '3.2':
        X = load_dataset('clusterData.pkl')['X']
        k=np.array([1,2,3,4,5,6,7,8,9,10])
        error_y=np.zeros(10)
        for i in k:
            error_np=np.zeros(50)
            for j in range(50):
                model=Kmeans(k=i)
                model.fit(X)
                error_np[j]=model.error(X)
            error_y[i-1]=np.min(error_np)
            
        plt.plot(k,error_y)
        fname = os.path.join("..", "figs", "k_elbow.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)
            

    elif question == '3.3':
        X = load_dataset('clusterData2.pkl')['X']
        model_list=[]
        error_np=np.zeros(50)
        for i in range(50):
            model=Kmeans(k=4)
            model.fit(X)
            model_list.append(model)
            error_np[i]=model.error(X)
        final_model=model_list[np.argmin(error_np)]
        plot_2dclustering(X,final_model.predict(X))
        fname = os.path.join("..", "figs", "q3_3.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)
        
    elif question == '3.3.3':
        X = load_dataset('clusterData2.pkl')['X']
#        k=np.array([1,2,3,4,5,6,7,8,9,10])
#        error_y=np.zeros(10)
#        for i in k:
#            error_np=np.zeros(50)
#            for j in range(50):
#                model=Kmeans(k=i)
#                model.fit(X)
#                error_np[j]=model.error(X)
#            error_y[i-1]=np.min(error_np)
#            
#        plt.plot(k,error_y)
#        fname = os.path.join("..", "figs", "k_elbow_3_3_3.png")
#        plt.savefig(fname)
#        print("\nFigure saved as '%s'" % fname)
        model_list=[]
        error_np=np.zeros(50)
        for i in range(50):
            model=Kmedian(k=4)
            model.fit(X)
            model_list.append(model)
            error_np[i]=model.error(X)
        final_model=model_list[np.argmin(error_np)]
        plot_2dclustering(X,final_model.predict(X))
        fname = os.path.join("..", "figs", "q3_3_3.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)

    elif question == '3.3.4':
        X = load_dataset('clusterData2.pkl')['X']
        k=np.array([1,2,3,4,5,6,7,8,9,10])
        error_y=np.zeros(10)
        for i in k:
            error_np=np.zeros(50)
            for j in range(50):
                model=Kmedian(k=i)
                model.fit(X)
                error_np[j]=model.error(X)
            error_y[i-1]=np.min(error_np)
            
        plt.plot(k,error_y)
        fname = os.path.join("..", "figs", "k_elbow_3_3_4.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)

    elif question == '3.4':
        X = load_dataset('clusterData2.pkl')['X']

        model = DBSCAN(eps=16, min_samples=3)
        y = model.fit_predict(X)

        print("Labels (-1 is unassigned):", np.unique(model.labels_))

        plot_2dclustering(X,y)
        fname = os.path.join("..", "figs", "clusterdata_dbscan.png")
        plt.savefig(fname)
        print("\nFigure saved as '%s'" % fname)


    elif question == '4':
        img = imread(os.path.join("..", "data", "mandrill.jpg"))

        for b in [1,2,4,6]:
            quantizer = ImageQuantizer(b)
            q_img = quantizer.quantize(img)
            d_img = quantizer.dequantize(q_img)

            plt.figure()
            plt.imshow(d_img)
            fname = os.path.join("..", "figs", "b_{}_image.png".format(b))
            plt.savefig(fname)
            print("Figure saved as '%s'" % fname)

            plt.figure()
            plt.imshow(quantizer.colors[None] if b/2!=b//2 else np.reshape(quantizer.colors, (2**(b//2),2**(b//2),3)))
            plt.title("Colours learned")
            plt.xticks([])
            plt.yticks([])
            fname = os.path.join("..", "figs", "b_{}_colours.png".format(b))
            plt.savefig(fname)
            print("Figure saved as '%s'" % fname)

    else:
        print("Unknown question: %s" % question)
