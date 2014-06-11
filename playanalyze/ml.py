import numpy as np
import pylab as pl
import math
from matplotlib.colors import ListedColormap
from sklearn import neighbors, cross_validation,datasets, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from prettytable import PrettyTable
from random import shuffle

#########################################################
######### Different Machine Learning Algorithms #########
#########################################################

PLAYS = {26:'ELBOW',42:'FLOPPY',53:'HORNS',92:'INVERT',98:'DELAY',32:'PUNCH',51:'DROP',7:'DRAG',501:'RANDOM'} # Used for Pretty Print

### Toggle Classifiers ###
KNN = True
SVM = True
ITERATIONS = 5

#########################################################
### Main Class To Run Classification Algorithm ##########
#########################################################
def runAnalysis(vectors,labels,possessionids):
    ### KNN Algorithm  ###
    if KNN:
        runKNN(vectors,labels,possessionids)
    ### SVM Algorithm ###
    if SVM:
        runSVM(vectors,labels,possessionids)
    return

#########################################################
######### KNN Classification Algorithm ##################
#########################################################
def runKNN(vectors,labels,possessionids):
    final_scores = []
    for number_of_nearest_neighbors in range(3,4):
        score = 0
        confusion_matrix = []
        for i in range(ITERATIONS):
            result = testClassifier(vectors,labels,possessionids,'kNearestNeighbors',number_of_nearest_neighbors,None,None)
            score += result['score']
            confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
        final_scores.append(round(score/ITERATIONS,2))
        print '\nKNN Confusion Matrix for K='+str(number_of_nearest_neighbors)
        prettyPrintConfusionMatrix(confusion_matrix,labels)
    print 'KNN with 3 NN: '+str(final_scores)


def kNeighborsClassifier(X_train,X_test,y_train,y_test,posid,variable1):
    n_neighbors = variable1
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
    clf.fit(X_train, y_train)
    right,wrong=0.0,0.0
    for c in range(len(X_test)):
        if clf.score(X_test[c],y_test[c]):
            right += 1
        else:
            wrong += 1
            # Following is used to get the possession id of a misclassified play
            #print "Wrongly Classified Pos "+str(posid[c])+": "+str(X_test[c])+":"+PLAYS[y_test[c]]+" | Predict: "+PLAYS[(clf.predict(X_test[c])[0])]
    cm = confusion_matrix(y_test, clf.predict(X_test))
    return {'score':right/(right+wrong),'confusion_matrix':cm}

#########################################################
######### SVM Classification Algorithm ##################
#########################################################
def runSVM(vectors,labels,possessionids):
    final_scores = []
    penalties = [1]
    for penalty in penalties: # Include a list of the penalty values you want to test over
        gamma_array = [1]
        for gamma in gamma_array:
            score = 0
            confusion_matrix = []
            for i in range(ITERATIONS):
                result = testClassifier(vectors,labels,possessionids,'SVM',penalty,gamma,'linear')
                score += result['score']
                confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
            final_scores.append(round(score/ITERATIONS,2))
            print '\nSVM Confusion Matrix for C='+str(penalty)
            prettyPrintConfusionMatrix(confusion_matrix,labels)
    for i in range(len(final_scores)):
        print "SVM with penalty "+str(penalties[i])+": "+str(final_scores[i])

def svmClassifier(X_train,X_test,y_train,y_test,penalty,gamma,kernel):
    clf = svm.SVC(C=penalty,kernel=kernel,gamma=gamma,probability=True)
    clf.fit(X_train, y_train)
    score = clf.score(X_test,y_test)
    cm = confusion_matrix(y_test, clf.predict(X_test))
    return {'score':clf.score(X_test,y_test),'confusion_matrix':cm}

#########################################################
######### One Vs. One Algorithm #########################
#########################################################
def oneVsoneAlgorithm():
    pass

def oneVsManyAlgorithm():
    pass
    
#########################################################
######### Test Classification Algorithm #################
#########################################################
def testClassifier(X,y,ids,method,variable1,variable2,variable3):
    #iris = datasets.load_iris()
    #X = iris.data
    #y = iris.target
    shuffled = shuffleList(X,y) # Shuffle the list to increase randomness
    X,y,ids = np.array(shuffled[0]),np.array(shuffled[1]),np.array(ids)
    skf = cross_validation.StratifiedKFold(y,3) # Test using stratified split
    score,count = 0,0
    confusion_matrix = []
    for train_index,test_index in skf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        posid = ids[test_index]
        if method == 'kNearestNeighbors':
            result = kNeighborsClassifier(X_train,X_test,y_train,y_test,posid,variable1)
        elif method == 'SVM':
            result = svmClassifier(X_train,X_test,y_train,y_test,variable1,variable2,variable3)
        score += result['score']
        count += 1
        confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
    return {'score':score/float(count),'confusion_matrix':confusion_matrix}

### Cascaded Classification Algorithm ###
def cascadedClassification(X_train,X_test,y_train,y_test):
    possible_outputs = list(set(sorted(y_train)))
    clfs = {} # Hold a list of the classifier objects
    # Train all the SVM Classifiers
    for po in possible_outputs:
        y_one_v_all = [(1 if num==po else 0) for num in y_train]
        classifier = svm.SVC()
        classifier.fit(X_train,y_one_v_all)
        clfs[po] = classifier
    # Run the test data through them
    for testpoint in range(len(X_test)):
        testpoint_x = X_test[testpoint]
        testpoint_y = y_test[testpoint]
        distances = {}
        for key,value in clfs.items():
            distance_to_hyperplane = value.decision_function(testpoint_x)[0][0] # Positive value means yes, negative means no
            distances[key] = distance_to_hyperplane
        calculateProbabilitiesFromHyperPlaneDistanceMeasures(distances,testpoint_y)
    print '------------------'

def RandomForestClassifier():
    iris = datasets.load_iris()
    clf = RandomForestClassifier(n_estimators=100)
    scores = cross_validation.cross_val_score(clf, iris.data, iris.target)
    print scores.mean() 


#########################################################
######### Pretty Print Functions  #######################
#########################################################

def prettyPrintSVM(final_scores,gamma_array):
    print '\nSVM Algorithm'
    top_row = ['']+["Gamma="+str(gamma) for gamma in gamma_array]
    x = PrettyTable(top_row)
    x.padding_width = 1 # One space between column edges and contents (default)
    for value in final_scores:
        x.add_row(value)
    print x

def prettyPrintKNN(final_scores):
    print '\nK Nearest Neighbors Algorithm'
    x = PrettyTable(["K=1", "K=2", "K=3","K=4","K=5","K=6"])
    #x = PrettyTable(["K=3"])
    x.padding_width = 1 # One space between column edges and contents (default)
    x.add_row(final_scores)
    print x

### Pretty Prints KNN Confusion Matrix ###
def prettyPrintConfusionMatrix(cm,axes):
    cm = normalizeArray(cm)
    print 'X Axis: Predicted Label, Y Axis: True Label'
    axes = list(sorted(set(axes)))
    toprow=['']
    for axe in axes:
        toprow.append(PLAYS[axe])
    x = PrettyTable(toprow)
    for i in range(len(cm)):
        x.add_row([PLAYS[axes[i]]]+cm[i])
    print x


#########################################################
######### Misc. Helper Functions  #######################
#########################################################
def classWeighter():
    weights = {}
    for key,value in PLAYS:
        weight[key] = 1 if value != 'RANDOM' else .2
    return weights

def confusionMatrixToList(cm):
    new_cm = []
    for row in cm:
        new_row = []
        for elem in row:
            new_row.append(elem)
        new_cm.append(new_row)
    return new_cm

### Takes in two arrays of arrays, and sums them ###
### Example: [[1,2],[3,4]]+[[5,6],[7,8]] = [[6,8],[10,12]] ###
def sumArrays(array_one,array_two):
    if not array_one and not array_two:
        return []
    if not array_one:
        return array_two
    if not array_two:
        return array_one
    final_array = []
    for i in range(len(array_one)):
        new_elem = []
        for j in range(len(array_one[0])):
            new_elem.append(array_one[i][j]+array_two[i][j])
        final_array.append(new_elem)
    return final_array

### Normalizes an array so the sum of all elements = new_sum ###
def normalizeArray(array):
    new_sum = 1000.0
    old_sum = sum(sum(row) for row in array)
    divider = max(old_sum/new_sum,1)
    for i in range(len(array)):
        for j in range(len(array[i])):
            array[i][j] = int(array[i][j]/divider)
    return array


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


#X = np.array([[1], [2], [3],[4],[5],[6],[7],[8],[9],[.5], [1.5], [2.5],[3.5],[4.5],[5.5],[6.5],[7.5],[8.5]])
#y = np.array([0, 0, 0,1,1,1,2,2,2,0,0,0,1,1,1,2,2,2])
