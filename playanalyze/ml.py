import numpy as np
import pylab as pl
from matplotlib.colors import ListedColormap
from sklearn import neighbors, cross_validation,datasets, svm 
from sklearn.metrics import confusion_matrix
from prettytable import PrettyTable
from random import shuffle
#########################################################
######### Different Machine Learning Algorithms #########
#########################################################
PLAYS = {26:'ELBOW',42:'FLOPPY',53:'HORNS',98:'INVERT',92:'DELAY',32:'PUNCH'}

def runAnalysis(vectors,labels,possessionids):
    #print possessionids
    iterations = 1
    # KNN Algorithm 
    final_scores = []
    for variable in range(1,7):
        final_score = sum([testClassifier(vectors,labels,possessionids,'kNearestNeighbors',variable,None,None) for i in range(iterations)])/float(iterations)
        final_scores.append(round(final_score,2))
    prettyPrintKMeans(final_scores)
    #SVM Algorithm
    final_scores = []
    gamma_array = [.1,.5,1,5]
    for penalty in [.5,1,5,10]:
        gammas = []
        for gamma in gamma_array:
            final_score = sum([testClassifier(vectors,labels,possessionids,'SVM',penalty,gamma,'linear') for i in range(iterations)])/float(iterations)
            gammas.append(round(final_score,2))
        final_scores.append(["C="+str(penalty)]+gammas)
    prettyPrintSVM(final_scores,gamma_array)
    return

def kNeighborsClassifier(X_train,X_test,y_train,y_test,posid,variable1):
    n_neighbors = variable1
    weights = 'distance' # Can be uniform or based on distance
    ### Run K-Nearest Neighbors Algorithm ###
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
    clf.fit(X_train, y_train)
    right,wrong=0.0,0.0
    for c in range(len(X_test)):
        if clf.score(X_test[c],y_test[c]):
            right += 1
        else:
            wrong += 1
            print "Wrongly Classified Pos "+str(posid[c])+": "+str(X_test[c])+":"+PLAYS[y_test[c]]+" | Predict: "+PLAYS[(clf.predict(X_test[c])[0])]
    cm = confusion_matrix(y_test, clf.predict(X_test))
    prettyPrintConfusionMatrix(cm,clf.predict(X_test))
    return right/(right+wrong)

def supportVectorMachine(X_train,X_test,y_train,y_test,penalty,gamma,kernel):
    clf = svm.SVC(C=penalty,kernel=kernel,gamma=gamma)
    clf.fit(X_train, y_train)
    return clf.score(X_test,y_test)

def testClassifier(X,y,ids,method,variable1,variable2,variable3):
    # Sample Data
    # X = [[1,4,3],[2,3,2],[1,3,1],[2,4,4],[8,3,5],[4,3,6],[1,4,7],[2,3,8],[1,3,9],[2,4,10],[8,3,11],[4,3,12]]
    # X = np.array(X)
    # y = np.array([0,1,2,0,2,1,0,1,2,0,2,1])
    X = np.array(X)
    y = np.array(y)
    ids = np.array(ids)
    #iris = datasets.load_iris()
    #X = iris.data
    #y = iris.target
    # Test using stratified split
    skf = cross_validation.StratifiedKFold(y,3)
    score = 0
    count = 0
    for train_index,test_index in skf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        posid = ids[test_index]
        if method == 'kNearestNeighbors':
            result = kNeighborsClassifier(X_train,X_test,y_train,y_test,posid,variable1)
        elif method == 'SVM':
            result = supportVectorMachine(X_train,X_test,y_train,y_test,variable1,variable2,variable3)
        score += result
        count += 1
        #print 'Round '+str(count)+": "+str(result)
        #print '----------------'
    return score/float(count)

def prettyPrintSVM(final_scores,gamma_array):
    print '\nSVM Algorithm'
    top_row = ['']+["Gamma="+str(gamma) for gamma in gamma_array]
    x = PrettyTable(top_row)
    x.padding_width = 1 # One space between column edges and contents (default)
    for value in final_scores:
        x.add_row(value)
    print x

def prettyPrintKMeans(final_scores):
    print '\nK Nearest Neighbors Algorithm'
    x = PrettyTable(["K=1", "K=2", "K=3","K=4","K=5","K=6"])
    #x = PrettyTable(["K=3"])
    x.padding_width = 1 # One space between column edges and contents (default)
    x.add_row(final_scores)
    print x

### Pretty Prints a Confusion Matrix ###
def prettyPrintConfusionMatrix(cm,axes):
    print '\nKNN Confusion Matrix'
    print 'X Axis: Predicted Label, Y Axis: True Label'
    axes = list(sorted(set(axes)))
    toprow=['']
    for axe in axes:
        toprow.append(PLAYS[axe])
    x = PrettyTable(toprow)
    cm_list = []
    for i in cm:
        cm_list.append(list(i))
    print cm_list
    for i in range(len(cm_list)):
        x.add_row([PLAYS[axes[i]]]+cm_list[i])
    print x

### Shuffles the List But Maintains order for tests and results ###
def shuffleList(X,y):
    int_list = [i for i in range(len(X))]
    shuffle(int_list)
    new_X = [0]*len(X)
    new_y = [0]*len(X)
    counter = 0
    for j in int_list:
        new_X[j] = X[counter]
        new_y[j] = y[counter]
        counter+=1
    return (new_X,new_y)

