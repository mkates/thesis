import numpy as np
import pylab as pl
import math
from matplotlib.colors import ListedColormap
from sklearn import neighbors, cross_validation,datasets, svm, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from prettytable import PrettyTable
from random import shuffle


#########################################################
######### Different Machine Learning Algorithms #########
#########################################################

PLAYS = {26:'ELBOW',42:'FLOPPY',53:'HORNS',92:'INVERT',98:'DELAY',32:'PUNCH',51:'DROP',7:'DRAG',501:'RANDOM',9:'POSTUP'} # Used for Pretty Print
PLAYS = {1:'PLAY',0:'NOT-PLAY'}
### Toggle Classifiers ###
KNN = False
SVM = True
OVO = False
OVA = False
RANKED = False
LEAVE_ONE_OUT = False
ITERATIONS = 1

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
    ### One v. One Algorithm
    if OVO:
        runOVO(vectors,labels,possessionids)
    ### One v. All Algorithm
    if OVA:
        runOVA(vectors,labels,possessionids)
    ### Ranking Algorithm
    if RANKED:
        runRANKED(vectors,labels,possessionids)
    ### Leave One Out Testing Algorithm
    if LEAVE_ONE_OUT:
        runLOO(vectors,labels,possessionids)
        #runLOO([[1,2,3,4],[1,3,5,7],[1,4,7,10],[98,99,100,101]],[1,2,3,2],possessionids)
    return

#########################################################
######### Leave One Out Algorithm #######################
#########################################################


def runLOO(vectors,labels,possessionids):
    print '---------------------------'
    print 'Leave One Out OVA Algorithm'
    average_score = 0.0
    counter = 0.0
    for index,vector in enumerate(vectors):
        ### Pop out the index to create the training and test data ###
        tmp_vectors = vectors[:]
        X_test= [tmp_vectors.pop(index)]
        X_train = tmp_vectors
        tmp_labels = labels[:]
        y_test= [tmp_labels.pop(index)]
        y_train = tmp_labels
        results = ovaClassifier(X_train,X_test,y_train,y_test)
        average_score += results['score']
        counter += 1
        if counter % 50 == 0:
            print counter
    print 'FINAL SCORE: '+str(average_score/counter)
    return

#########################################################
######### Ranking Algorithm #############################
#########################################################

def runRANKED(vectors,labels,possessionids):
    X,y,ids = vectors,labels,possessionids
    unique_labels = len(set(labels))
    ### Keep a dictionary of each play and number of first and second correct guesses
    correct = [0]*unique_labels
    individual_plays = {}
    for key,value in PLAYS.items():
        individual_plays[key] = [0]*unique_labels
    for i in range(ITERATIONS):
        shuffled = shuffleList(X,y) # Shuffle the list to increase randomness
        X,y,ids = np.array(shuffled[0]),np.array(shuffled[1]),np.array(ids)
        skf = cross_validation.StratifiedKFold(y,5) # Test using stratified split
        score,count = 0,0
        for train_index,test_index in skf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            results = ovaClassifier(X_train,X_test,y_train,y_test)
            all_results = results['all_results']
            labels = results['labels']
            for idx in range(len(all_results)):
                guesses = [elm[2] for elm in sorted(all_results[idx]['results'],reverse=True)]
                label = labels[idx]
                index = guesses.index(label)
                correct[index] += 1
                individual_plays[label][index] += 1
    print '\n Ranked Performance (i.e. When elbow was the result, you guessed it correctly X times on the first try and Y times on the second try)'
    x = PrettyTable(['']+["Guess #"+str(i) for i in range(1,unique_labels+1)])
    for idx,value in enumerate(set(labels)):
        x.add_row([PLAYS[value]]+individual_plays[value])
    x.padding_width = 1 # One space between column edges and contents (default)
    print x
    print '\nRanked For Performance'
    print [str(round(correct[idx]*100/float(sum(correct)),1))+"%" for idx,value in enumerate(correct)]
    #x.add_row()
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
            #print "Wrongly Classified Pos "+str(posid[c])+": "+str(X_test[c])+":"+PLAYS[y_test[c]]+" | Predict: "+PLAYS[(clf.predict(X_test[c])[0])]
    cm = confusion_matrix(y_test, clf.predict(X_test))
    return {'score':right/(right+wrong),'confusion_matrix':cm}

#########################################################
######### SVM Classification Algorithm ##################
#########################################################
def runSVM(vectors,labels,possessionids):
    final_scores = []
    penalties = [.1,1]
    class_weight = [1,3]
    for penalty in penalties: # Include a list of the penalty values you want to test over
        for gamma in class_weight:
            score = 0
            confusion_matrix = []
            for i in range(ITERATIONS):
                result = testClassifier(vectors,labels,possessionids,'SVM',penalty,gamma,'linear')
                score += result['score']
                confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
            final_scores.append(round(score/ITERATIONS,2))
            print '\nSVM Confusion Matrix for C='+str(penalty)
            prettyPrintConfusionMatrix(confusion_matrix,labels)
    for i in range(len(penalties)):
        for j in range(len(class_weight)):
            print "SVM with penalty "+str(penalties[i])+" and class weight "+str(class_weight[j])+": "+str(final_scores[i*j])

def svmClassifier(X_train,X_test,y_train,y_test,penalty,gamma,kernel):
    clf = svm.SVC(C=penalty,kernel=kernel,gamma=gamma,probability=True)
    clf.fit(X_train, y_train)
    score = clf.score(X_test,y_test)
    cm = confusion_matrix(y_test, clf.predict(X_test))
    return {'score':clf.score(X_test,y_test),'confusion_matrix':cm}

#########################################################
######### One Vs. One Algorithm #########################
#########################################################

def runOVO(vectors,labels,possessionids):
    score = 0
    confusion_matrix = []
    for i in range(ITERATIONS):
        result = testClassifier(vectors,labels,possessionids,'OVO',None,None,None)
        score += result['score']
        confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
    final_score = round(score/ITERATIONS,2)
    print '\nOVO Confusion Matrix'
    prettyPrintConfusionMatrix(confusion_matrix,labels)
    print 'OVO Score: '+str(final_score)

def ovoClassifier(X_train,X_test,y_train,y_test):
    # 1. Generate an SVM for every unique pair (excluding random examples)
    X_trained, y_trained = removeRandomSamples(X_train,y_train)
    unique_pairs = uniquePairs(list(set(sorted(y_trained)))) # Generates all unique pairs in a list
    for unique_pair in unique_pairs:
        filtered_data = filterTrainingData(X_trained,y_trained,unique_pair[0],unique_pair[1])
        clf = svm.SVC(C=1,kernel='linear',probability=True)
        clf.fit(filtered_data[0],filtered_data[1])
        unique_pair[2] = clf
    
    # 2. Run every training point through the SVM to generate a probability chart
    new_training_data = []
    for idx,val in enumerate(y_train):
        probabilities = []
        for up in unique_pairs:
            probability = up[2].predict_proba(X_train[idx])
            probabilities.append(probability[0][0])
        new_training_data.append(probabilities)
    
    # 3. Run an SVM with the confidence outputs of each training point
    ultimate_clf = svm.SVC(C=1,kernel='linear')
    ultimate_clf.fit(new_training_data,y_train)
    
    # 4. Run every test point through the SVMs to generate a probability chart
    new_data = []
    for idx, test_point in enumerate(y_test):
        new_probability_data = []
        for up in unique_pairs:
            probability = up[2].predict_proba(X_test[idx])
            new_probability_data.append(probability[0][0])
        new_data.append(new_probability_data)
    new_data = np.array(new_data)    
    cm = confusion_matrix(y_test, ultimate_clf.predict(new_data))
    return {'score':ultimate_clf.score(new_data,y_test),'confusion_matrix':cm}



## Filters training data to only the two labels for running a one v one algorithm ###
def filterTrainingData(X_train,y_train,label1,label2):
    filtered_x_train = []
    filtered_y_train = []
    for idx, val in enumerate(y_train):
        if (val==label1 or val==label2):
            filtered_x_train.append(X_train[idx])
            filtered_y_train.append(y_train[idx])
    return (filtered_x_train,filtered_y_train)

def removeRandomSamples(X_train,y_train):
    filtered_x_train = []
    filtered_y_train = []
    for idx, val in enumerate(y_train):
        if val!=501:
            filtered_x_train.append(X_train[idx])
            filtered_y_train.append(y_train[idx])
    return (filtered_x_train,filtered_y_train)

def onlyRandomSamples(X_train,y_train):
    filtered_x_train = []
    filtered_y_train = []
    for idx, val in enumerate(y_train):
        if val==501:
            filtered_x_train.append(X_train[idx])
            filtered_y_train.append(y_train[idx])
    return (filtered_x_train,filtered_y_train)


#########################################################
######### One Vs. ALL Algorithm #########################
#########################################################


def runOVA(vectors,labels,possessionids):
    score = 0
    confusion_matrix = []
    correct_bucket = []
    total_bucket = []
    for i in range(ITERATIONS):
        result = testClassifier(vectors,labels,possessionids,'OVA',None,None,None)
        score += result['score']
        confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
        correct_bucket = ([ x1+y1 for x1,y1 in zip(correct_bucket, result['correct_bucket'])] if correct_bucket else result['correct_bucket'])
        total_bucket = ([ x1+y1 for x1, y1 in zip(total_bucket, result['total_bucket'])] if total_bucket else result['total_bucket'])
    print '\nConfidence Buckets'
    confidence_bucket = [(round(float(ai)/bi,2) if bi>0 else 0) for ai,bi in zip(correct_bucket,total_bucket)]
    printConfidenceBuckets(confidence_bucket,[round(float(tb)/sum(total_bucket),2) for tb in total_bucket])
    final_score = round(score/ITERATIONS,2)
    print '\nOVA Confusion Matrix'
    #prettyPrintConfusionMatrix(confusion_matrix,labels)
    print 'OVA Score: '+str(final_score)

def printConfidenceBuckets(confidence_bucket,total_bucket):
    headers = ['Confidence']
    for i in range(len(confidence_bucket)):
        headers.append(str(int(i*100/len(confidence_bucket)))+'-'+str(int((i+1)*100/len(confidence_bucket)))+'%')
    x = PrettyTable(headers)
    x.padding_width = 1 # One space between column edges and contents (default)
    x.add_row(['Correctness']+confidence_bucket)
    x.add_row(['Percent of Samples']+total_bucket)
    print x

def ovaClassifier(X_train,X_test,y_train,y_test):
    # 1. Generate an SVM for every label and its complement
    labels = list(set(sorted(y_train)))
    if 501 in labels:
        labels.remove(501) # enable if using random
    svm_dict = {}
    for label in labels:
        new_y_train = [(1 if y==label else 0) for y in y_train]
        clf = svm.SVC(C=1,class_weight={1:3,0:1},probability=True)
        clf.fit(X_train,new_y_train)
        svm_dict[label] = clf
    # 2. Now Run every test point through each one vs. all
    all_results = []
    for idx,val in enumerate(y_test):
        results = []
        for key,value in svm_dict.items():
            prediction = value.predict(X_test[idx])[0]
            probability = value.predict_proba(X_test[idx])[0][1]
            prediction = (1 if probability > .5 else 0)
            results.append((prediction,probability,key))
        all_results.append({'results':results,'label':val})
    
    # 3. Generate guesses, labels, and confidence arrays (for scoring)
    guesses = []
    labels = []
    confidence = []
    for all_result in all_results:
        prediction = predictOVA(all_result)
        guesses.append(prediction['handle'])
        if prediction['pos_probability'] > 0:
            confidence.append(prediction['pos_probability'])
        else:
            confidence.append(1.0-prediction['neg_probability'])
        labels.append(all_result['label'])

    #4. Score 
    correct_buckets = [0]*10
    total_buckets = [0]*10
    for i in range(len(guesses)):
        score = (1 if guesses[i]==labels[i] else 0)
        bucket = int(math.floor(confidence[i]*10))
        correct_buckets[bucket] += score
        total_buckets[bucket] += 1
    score = sum([(1 if guesses[i]==labels[i] else 0) for i in range(len(guesses))])/float(len(guesses))
    guesses = np.array(guesses)
    cm = confusion_matrix(labels, guesses)
    return {'score':score,'confusion_matrix':cm,'all_results':all_results,'labels':labels,'correct_bucket':correct_buckets,'total_bucket':total_buckets}


## Given the probabilities from each SVM, get the prediction ##
def predictOVA(outcome):
    count = 0
    highest_pos_prob = 0
    highest_neg_prob = 0
    handle = 501
    for rank in outcome['results']:
        #if rank[1] > highest_pos_prob:
        if rank[1] > .5 and rank[1] > highest_pos_prob:
            highest_pos_prob = rank[1]
            handle = rank[2]
            count += 1
        else:
            highest_neg_prob = max(highest_neg_prob,rank[1])
    return {'handle':handle,'pos_probability':highest_pos_prob,'neg_probability':highest_neg_prob}

#########################################################
######### Test Classification Algorithm #################
#########################################################
def testClassifier(X,y,ids,method,variable1,variable2,variable3):
    #iris = datasets.load_iris()
    #X = iris.data
    #y = iris.target
    shuffled = shuffleList(X,y) # Shuffle the list to increase randomness
    X,y,ids = np.array(shuffled[0]),np.array(shuffled[1]),np.array(ids)
    skf = cross_validation.StratifiedKFold(y,5) # Test using stratified split
    score,count = 0,0
    confusion_matrix = []
    correct_bucket = []
    total_bucket = []
    for train_index,test_index in skf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        posid = ids[test_index]
        if method == 'kNearestNeighbors':
            result = kNeighborsClassifier(X_train,X_test,y_train,y_test,posid,variable1)
        elif method == 'SVM':
            result = svmClassifier(X_train,X_test,y_train,y_test,variable1,variable2,variable3)
        elif method == 'OVO':
            result = ovoClassifier(X_train,X_test,y_train,y_test)
        elif method == 'OVA':
            result = ovaClassifier(X_train,X_test,y_train,y_test)
        score += result['score']
        count += 1
        confusion_matrix = sumArrays(confusion_matrix,confusionMatrixToList(result['confusion_matrix']))
        #correct_bucket = ([ x1+y1 for x1,y1 in zip(correct_bucket, result['correct_bucket'])] if correct_bucket else result['correct_bucket'])
        #total_bucket = ([ x1+y1 for x1, y1 in zip(total_bucket, result['total_bucket'])] if total_bucket else result['total_bucket'])
    return {'score':score/float(count),'confusion_matrix':confusion_matrix,'correct_bucket':correct_bucket,'total_bucket':total_bucket}


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

def prettyPrintGrid(y_axis,x_axis,values):
    x_label = ['']+x_axis
    x = PrettyTable(x_label)
    for index,label in enumerate(y_axis):
        x.add_row([label]+values[index])
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

### Given a list, generates all unique pairs in a list of tuples of length 3 ###
def uniquePairs(list_of_labels):
    unique_pairs_list = []
    list_of_labels = sorted(list_of_labels)
    for i in range(len(list_of_labels)):
        for j in range(len(list_of_labels)):
            if j < i:
                unique_pairs_list.append([list_of_labels[j],list_of_labels[i],None])
    return unique_pairs_list

#X = np.array([[1], [2], [3],[4],[5],[6],[7],[8],[9],[.5], [1.5], [2.5],[3.5],[4.5],[5.5],[6.5],[7.5],[8.5]])
#y = np.array([0, 0, 0,1,1,1,2,2,2,0,0,0,1,1,1,2,2,2])
