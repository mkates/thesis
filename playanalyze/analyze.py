from playanalyze.models import *
from playanalyze.helper import *
import playanalyze.ml as ml
import math
import inspect as inspect
import numpy as np
import pylab as pl
import math
from matplotlib.colors import ListedColormap
from sklearn import neighbors, cross_validation,datasets, svm, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from prettytable import PrettyTable
import random as random
##########################################################
######### Hand Extracted Plays That Are Run Well #########
##########################################################
# Lengths: POSTUP (63), ELBOW (61), FLOPPY (74), HORNS (32), INVERT (39), DELAY (80), RANDOM (196)
#npu = 9474
POSTUP = [217,282,326,934,1221,1227,1247,1261,2735,2763,3208,3222,3250,3269,3419,3934,4585,4638,5140,5406,5426,5844,6048,6052,6198,6291,6354,6664,6774,7064,7367,8539,8573,8672,8701,8740,8784,8800,9247,9259,9474,9572,9816,9826,9834,9859,10087,7382,4614,9253,5749,8760,5188,9294,4179,5719,6676,8838,6289,9362,6301,183,9439,4425,5477,10093,9214]
POSTUP_TIMES={
217:490,
282:521.8,
326:581.3,
934:131,
941:683,
1221:552,
1227:387.5,
1247:486.5,
1261:55.38,
2735:605.5,
2763:454.9,
3208:575.2,
3222:160.5,
3250:693.7,
3255:527.2,
3269:86.5,
3419:317.0,
3934:461.5,
4133:627,
4585:146.3,
4638:465,
5140:371.7,
5144:224.5,
5406:415.5,
5426:549.2,
5844:457.25,
6048:148,
6052:40,
6154:549.2,
6167:161.7,
6198:672,
6291:530.4,
6354:356,
6664:431.5,
6774:658.2,
7022:606.5,
7064:118.2,
7367:211.5,
8539:582.5,
8573:291.3,
8672:516.3,
8701:294,
8740:340.2,
8751:650,
8784:441.2,
8800:638.8,
9247:66.3,
9259:393.8,
9474:273.7,
9572:43.8,
9816:433.6,
9826:86.7,
9834:511.5,
9835:478.2,
9859:535,
10087:65.7,
7382:457.7, # Start of Post Ups from from Random
4614:590.5,
9253:575.9,
5749:85,
8760:400,
5188:374.5,
9294:45,
4179:675,
5719:372,
6676:694,
8838:312,
6289:610.3,
9362:136.5,
6301:169,
183:165.8,
9439:650.5,
4425:475,
5477:245.7,
10093:607.5,
9214:370.5,
}
ELBOW = [100,137,201,306,968,1200,3398,3426,3435,3438,3444,4118,4136,4180,4182,4184,4411,4434,4485,4579,4582,4646,5214,5451,5590,5592,5631,5637,5706,5735,5855,6025,6205,6251,6299,6300,6315,6318,7004,7008,7080,7356,7366,7376,7385,7387, 7389, 7394, 7423, 7460, 8769, 8773, 8794, 8980, 9158, 9170, 9204, 9348, 9383, 9396, 9555, 9808, 9838, 9844, 9845, 9871]
ELBOW_TIMES = {
100:621,
137:172,
201:359,
306:496.5,
968:599,
1200:579,
3398:264,
3426:85,
3435:595.5,
3438:496,
3444:308.5,
4118:338,
4136:547,
4180:651,
4182:586,
4184:508.3,
4411:271.5,
4434:183,
4485:342.5,
4579:399,
4582:283,
4646:205.5,
5214:223,
5451:344,
5590:149,
5592:89.3,
5631:327.4,
5637:130.5,
5706:101.4,
5735:538.4,
5855:146,
6025:182,
6205:438.2,
6251:436.5,
6299:259.8,
6300:211.2,
6315:317.8,
6318:220.5,
7004:373.5,
7008:293,
7080:229,
7356:538.2,
7366:243,
7376:620.2,
7385:366,
7387:365.8,
7389:236.8,
7394:124,
7423:211,
7460:46,
8769:161.3,
8773:45.3,
8794:117,
8980:173.4,
9158:385.6,
9170:36.3,
9204:711.6,
9348:582.5,
9383:258.4,
9396:555.2,
9555:619.4,
9808:607.1,
9838:403.4,
9844:248.2,
9845:220.7,
9871:173.6
}
FLOPPY = [111,117,190,198,200,292,338,350,499,519,920,921,927,971,990,1213,1253,2751,2771,2787,3367,3401,3921,3942,3943,3944,3946,3983,3985,4003,4004,4120,4135,4145,4412,4416,4423,4428,4433,4478,4603,5142,5196,5436,5649,5843,5871,6026,6043,6064,6264,6672,6673,6713,7009,7026,7028,7355,7406,8771,8973,8999,9129,9237,9241,9281,9287,9453,9798,10101]
FLOPPY_TIMES={
111:284,
117:79,
190:667,
198:448.2,
200:395,
292:209,
338:229.5,
350:201.7,
499:429,
519:502.3,
920:544.75,
921:511.3,
927:340.4,
971:519,
990:586.2,
1213:127,
1253:309.3,
2751:160.1,
2771:230,
2787:428.6,
3367:569.2,
3401:180.5,
3921:194.5,
3942:184.8,
3943:148,
3944:123.5,
3946:64.7,
3983:309.5,
3985:262.8,
4003:402.5,
4004:355.8,
4120:282.4,
4135:563.3,
4145:259,
4412:245,
4416:113,
4423:533,
4428:401.8,
4433:212,
4478:583.4,
4603:215.6,
5142:311.3,
5196:117,
5436:169.3,
5649:468.3,
5843:495.5,
5871:265.1,
6026:141.5,
6043:299.6,
6064:403,
6264:42.5,
6672:80,
6673:43.8,
6713:247.8,
7009:260.8,
7026:492.3,
7028:417.4,
7355:560.2,
7406:422.4,
8771:97.2,
8973:436.2,
8999:310.4,
9129:486.3,
9237:386.2,
9241:275.1,
9281:436.8,
9287:271.5,
9453:184.1,
9798:187.6,
10101:360
}
HORNS = [1210,1211,1212,1243,1258,2826,4137,4138,4183,4488,5477,5737,5921,6346,7027,8845,9164,9196,9208,9213,9219,9786]
HORNS_TIMES = {
1210:221.8,
1211:196.2,
1212:163.8,
1243:603,
1258:159,
2826:40.6,
4137:4137,
4138:497,
4183:549.3,
4488:232.4,
5477:246.4,
5737:460.5,
5921:144,
6346:674.8,
7027:440.3,
8845:117.3,
9164:216.8,
9196:204.4,
9208:584.2,
9213:406.4,
9219:191,
9786:525.4
}
INVERT=[107,334,919,1202,1204,1249,3237,3836,3933,3939,4113,4399,4403,4425,4447,4481,4490,4614,4655,5660,5661,5680,5700,5719,5724,5842,6086,6231,7030,8812,9014,9147,9192,9230,9264,10114,10134]
INVERT_TIMES  = {
107:411.6,
334:335,
919:569,
1202:485.1,
1204:400,
1249:423.3,
3237:400.6,
3836:675.1,
3933:492,
3939:296.3,
4113:485.8,
4399:591.3,
4403:493.4,
4425:476.2,
4447:488,
4481:463,
4490:179.5,
4614:593.8,
4655:238.5,
5660:121,
5661:96.3,
5680:230,
5700:303.5,
5719:374.7,
5724:197,
5842:521.3,
6086:389.2,
6231:363.8,
7030:369.5,
8812:281.5,
9014:588.8,
9147:689,
9192:39.4,
9230:574.8,
9264:257.2,
10114:611.5,
10134:659
}
DELAY = [118,215,323,1194,2749,2785,2788,3212,3236,3244,3853,3870,3906,3907,3908,3909,3920,3974,4006,4442,4634,4636,4654,5138,5139,5441,5617,5626,5627,5628,5712,5733,5888,5899,5912,5916,6080,6131,6134,6168,6182,6188,6201,6268,6312,6317,6334,6719,6999,7069,7071,7084,7400,7431,7454,7458,8564,8732,8735,8770,8825,8826,8827,8969,8970,8971,8989,9060,9163,9177,9211,9212,9218,9258,9298,9302,9333,9397,9398,9399,9400,9404,9486,9492,9493,9494,9527,9557,9570,9581,9875,10133]
DELAY_TIMES = {
118:42.5,
215:144.9,
323:682.3,
1194:43.3,
2749:221.5,
2785:498,
2788:394.7,
3212:460.2,
3236:269,
3244:182.8,
3853:160,
3870:331.3,
3906:639.2,
3907:606.3,
3908:568.3,
3909:523.5,
3920:216.5,
3974:589.4,
4006:261.4,
4442:674.7,
4634:620.3,
4636:537,
4654:2734,
5138:437.4,
5139:401.6,
5441:689.7,
5617:46.3,
5626:491.9,
5627:450.4,
5628:417.5,
5712:648.5,
5733:594,
5888:510.8,
5899:163,
5912:416,
5916:283,
6080:599.6,
6131:539,
6134:443.6,
6168:116.3,
6182:414.2,
6188:250,
6201:546,
6268:633,
6312:420.5,
6317:245,
6334:412.2,
6719:101.3,
6999:504.9,
7069:663.4,
7071:586.5,
7084:137.6,
7400:633.8,
7431:679.4,
7454:236.8,
7458:96.5,
8564:545.3,
8732:575.4,
8735:474,
8770:141,
8825:687.1,
8826:655.4,
8827:619.2,
8969:578.9,
8970:550,
8971:506.8,
8989:593.2,
9060:618.3,
9163:259.5,
9177:544,
9211:465,
9212:439.9,
9218:223,
9258:424.1,
9298:629.3,
9302:487.2,
9333:322.3,
9397:517.2,
9398:489.2,
9399:460.4,
9400:425.7,
9404:280.2,
9486:628.9,
9492:424.5,
9493:3381.6,
9494:337.9,
9527:711.6,
9557:539,
9570:128.2,
9581:471.7,
9875:71.2,
10133:694.3
}
### USE AS NOISE (NOT HAND LOOKED AT TO ENSURE THEY RAN THE PLAY) ###

DROP = [159, 170, 242, 308, 352, 359, 527, 918, 928, 932, 938, 967, 983, 984, 2773, 2789, 3865, 3866, 3977, 3979, 4007, 4008, 4165, 4668, 4669, 5141, 5158, 5453, 5603, 5650, 5696, 5865, 5869, 5908, 6033, 6057, 6083, 6128, 6162, 6163, 6224, 6230, 6322, 6350, 6352, 6679, 6696, 6781, 7003, 7054, 7079, 7449, 7450, 7787, 8548, 8703, 8707, 8708, 8730, 8731, 8736, 8768, 8958, 8972, 9019, 9111, 9352, 9353, 9356, 9379, 9815, 9847]
DROP_TIMES = []
DRAG = [157, 227, 2809, 3388, 3446, 3837, 4011, 4663, 5407, 5444, 5620, 6158, 6302, 7057, 7403, 8792, 9029, 9326, 9436, 9441, 9848]
DRAG_TIMES = []
RANDOM = [154, 167, 180, 193, 202, 214, 230, 232, 289, 290, 297, 336, 916, 931, 943, 986, 1000, 1008, 1199, 1201, 1209, 1245, 2746, 2759, 2766, 2768, 2772, 2774, 2795, 2802, 3195, 3200, 3211, 3235, 3240, 3241, 3256, 3259, 3263, 3839, 3850, 3887, 3914, 3931, 3954, 3980, 4111, 4126, 4146, 4150, 4161, 4186, 4188, 4193, 4467, 4480, 4482, 4599, 4628, 4635, 4642, 4644, 4659, 4686, 5150, 5159, 5168, 5188, 5191, 5215, 5219, 5404, 5434, 5438, 5442, 5446, 5601, 5644, 5732, 5736, 5740, 5742, 5748, 5749, 5863, 5879, 5880, 5903, 5905, 6050, 6056, 6060, 6072, 6074, 6099, 6136, 6149, 6161, 6173, 6177, 6181, 6187, 6189, 6216, 6217, 6260, 6273, 6289, 6297, 6301, 6308, 6326, 6333, 6342, 6640, 6644, 6652, 6659, 6668, 6676, 6678, 6702, 6994, 7015, 7039, 7044, 7055, 7060, 7076, 7365, 7382, 7386, 7401, 7409, 7417, 7429, 7745, 7746, 7750, 7786, 8550, 8673, 8683, 8695, 8727, 8760, 8783, 8788, 8793, 8838, 8962, 9007, 9026, 9085, 9127, 9130, 9131, 9133, 9161, 9169, 9199, 9214, 9220, 9253, 9286, 9294, 9301, 9311, 9313, 9325, 9330, 9355, 9360, 9362, 9391, 9394, 9395, 9401, 9428, 9430, 9439, 9482, 9521, 9532, 9582, 9787, 9794, 9802, 9809, 9821, 10104, 10107, 10113, 10118, 10127, 10131]
RANDOM_FILTERED = [167,180,193,202,203,232,289,333,336,916,986,1008,1189,1199,1205,1245,2746,2766,2774,3183,3188,3195,3200,3211,3217,3235,3240,3263,3403,3433,3839,3847,3850,3881,3914,3931,3954,3980,4111,4150,4161,4186,4193,4194,4467,4599,4635,4642,4644,4659,4686,5185,5188,5191,5199,5215,5219,5404,5434,5438,5442,5601,5644,5681,5742,5903,6072,6099,6136,6161,6173,6216,6289,6297,6326,6342,6640,6644,6652,6659,6678,6994,7044,7055,7386,7417,8550,8670,8673,8683,8695,8727,8788,8962,9007,9085,9161,9169,9277,9286,9301,9313,9325,9428,9430,9439,9482,9521,9532,9582,9787,9794,9802,10079,10104,10107,10118,10127]
RANDOM_TIMES = []

PLAYS = {26:'ELBOW',42:'FLOPPY',53:'HORNS',92:'INVERT',98:'DELAY',51:'DROP',7:'DRAG',9:'POSTUP',501:'RANDOM'}
MANUAL_TIMES = {26:ELBOW_TIMES,42:FLOPPY_TIMES,53:HORNS_TIMES,92:INVERT_TIMES,98:DELAY_TIMES,51:DROP_TIMES,7:DRAG_TIMES,9:POSTUP_TIMES,501:RANDOM_TIMES}
LENGTHS = {26:3,42:5,53:4,92:2,98:3,32:6,51:6,7:6,9:2,501:6} #The typical length of the play

#####################################
####### Generate Base Positions #####
#####################################

def basePositions():
	dic = {'RANDOM':RANDOM_FILTERED,'ELBOW':ELBOW,'FLOPPY':FLOPPY,'HORNS':HORNS,'INVERT':INVERT,'DELAY':DELAY,'POSTUP':POSTUP}
	for key,value in dic.iteritems():
		relevant_possession_ids = value
		possessions = Possession.objects.filter(id__in=relevant_possession_ids)
		for possession in possessions:
			try:
				possession.positions = getPositions(possession)
				possession.play_id = [keys for keys,val in PLAYS.items() if val==key][0] # Reverse assign play ids in case they are mislabeled
			except:
				print possession.id
		print str(key)+" complete"
		dic[key] = list(possessions)
	#ALL = list(dic['FLOPPY'])+list(dic['INVERT'])+list(dic['HORNS'])+list(dic['ELBOW'])+list(dic['DELAY'])+list(dic['DROP'])+list(dic['DRAG'])+list(dic['RANDOM'])
	#ALL = list(dic['FLOPPY'])+list(dic['INVERT'])+list(dic['HORNS'])+list(dic['ELBOW'])+list(dic['DELAY'])+list(dic['RANDOM'])+list(dic['POSTUP'])
	return dic

#####################################
####### Main Run Function ###########
#####################################

def run(basePositions):
	vectors,results,possessionids = [],[],[]
	count = 0
	for possession in basePositions:
		if possession.play.play_id == 9:
			play_id = 1
		else:
			play_id = 0
		#play_id = possession.play.play_id
		vector = buildUniqueMeasureVectors(possession.positions)+buildSequenceClosenessVectors(possession.positions)+buildPositionVectors(possession.positions)+buildPassVectors(possession.positions)
		vectors.append(vector)
		results.append(play_id)
		possessionids.append(possession.id)

	ml.runAnalysis(vectors,results,possessionids)
	# for i in range(len(vectors)):
	# 	print str(vectors[i])+": "+str(results[i])
	print "\nVector Length: "+str(len(vector))
	print '\nANALYSIS COMPLETE'
	#return (vectors,results)

#######################################################################
####### Compares the different styles 6 second vs variable second #####
#######################################################################

########### The function to call to compare the styles ##############
def runDifferent(basePositions):
	# 1. Shuffle and filter out bad examples (less than 2 seconds long)
	random.shuffle(basePositions)
	basePositions = [basePosition for basePosition in basePositions if basePosition.positions['play_start']-basePosition.positions['play_end'] > 2]
	# 2. Stratified split of the examples
	labels = [basePosition.play.play_id for basePosition in basePositions]
	skf = cross_validation.StratifiedKFold(labels,2)
	# 3. Iterate through each stratified training example
	#scoreWindowedML(basePositions,skf,PLAY_TO_TEST)

	scoreFullLengthML(basePositions,skf)
	scoreMultiClassWindowedML(basePositions,skf)
	return 'COMPLETE'

########### Scores the Full Length ML Using OVA Strategy ##############
def scoreFullLengthML(basePositions,skf):
	#labels = list(set([possession.play_id for possession in basePositions if possession.play_id != 501])) # List of unique play IDs
	TIMES = [0,1,2,3,4,5,6]
	results = []
	for train_index,test_index in skf:
		# Generate the SVMs from the training examples
		train_set = retrieveIndexes(basePositions,list(train_index))
		training_vectors = [buildVector(possession.positions,TIMES,False) for possession in train_set]
		training_labels = [possession.play_id for possession in train_set]
		training_labels_set = set(training_labels)
		if 501 in training_labels_set: # Remove 501 from the svm generation if its part of the training_labels
			training_labels_set.remove(501)

		# Generate the SVMs
		svms = {}
		for label in training_labels_set:
			unit_training_labels = [(1 if label==val else 0) for val in training_labels] # Convert labels to 1's and 0's
			clf = svm.SVC(C=10,kernel='rbf',probability=True)
			clf.fit(training_vectors, unit_training_labels)
			svms[label] = clf

		# Test them 
		test_set = retrieveIndexes(basePositions,list(test_index))
		test_vectors = [buildVector(possession.positions,TIMES,False) for possession in test_set]
		test_labels = [possession.play_id for possession in test_set]
		for index,test_point in enumerate(test_vectors):
			highest_probability = 0
			highest_probability_value = 0
			for key,value in svms.items():
				probability = svms[key].predict_proba(test_point)
				probability = probability[0].tolist()[1]
				highest_probability = key if highest_probability_value < probability else highest_probability
				highest_probability_value = max(probability,highest_probability_value)
			if highest_probability_value > .25:
				results.append((highest_probability,test_labels[index]))
			else:
				results.append((501,test_labels[index]))

	print '\nFull Length Confusion Matrix Performance'
	return resultGeneration(results)

########### This is the one vs all algorithm with windowed algorithm ##############
def scoreWindowedML(basePositions,skf,PLAY_TO_TEST):
	training_confusion = [[0,0],[0,0]]
	confusion = [[0,0],[0,0]]
	correct,total = 0,0
	TIMES = [0,1,2]
	pass_1,pass_2 = [0,0,0,0,0,0],[0,0,0,0,0,0]
	grr = []
	for train_index,test_index in skf:
		# 4. Generate training and test sets
		train_set = retrieveIndexes(basePositions,list(train_index))
		test_set = retrieveIndexes(basePositions,list(test_index))
		# Generate window_possessions from sliding window scale
		training_vectors = []
		for possession in train_set:
			if possession.play_id == PLAY_TO_TEST:
				if possession.id in POSTUP_TIMES.keys():
					training_vectors.append((convertgetPositionToCustomTime(possession.positions,POSTUP_TIMES[possession.id],POSTUP_TIMES[possession.id]-2),1,possession.id))
					#training_vectors.append((convertgetPositionToCustomTime(possession.positions,POSTUP_TIMES[possession.id]+.5,POSTUP_TIMES[possession.id]-1.5),1,possession.id))
					#training_vectors.append((convertgetPositionToCustomTime(possession.positions,POSTUP_TIMES[possession.id]-.5,POSTUP_TIMES[possession.id]-2.5),1,possession.id))
			else:
				window_possessions = windowPositionsFromGetPositions(possession.positions,2,.5)
				for positions in window_possessions:
					training_vectors.append((positions,0,possession.id))
		# Convert position objects into machine learning vectors
		ml_vectors = []
		ml_labels = []
		ml_id = []
		for positions,label,id in training_vectors:
			printed = True if label==1 else False
			vector = buildVector(positions,TIMES,False)
			ml_vectors.append(vector)
			ml_labels.append(label)
			ml_id.append(id)
			# if label == 1:
			# 	pass_1 = [pass_1[i]+vector[i] for i in range(len(vector))]
			# 	if vector[3] == 0:
			# 		print buildVector(positions,TIMES,True)
			# 		print str(vector)+": "+str(label)+"  -  "+str(id)
			# 		grr.append(id)
			# 		print '-----------\n'
			# else:
			# 	pass_2 = [pass_2[i]+vector[i] for i in range(len(vector))]
		# Run the machine learning algorithms
		clf = svm.SVC(C=.3,class_weight={1:8,0:1},kernel='linear',probability=True)
		clf.fit(ml_vectors, ml_labels)

		# How dows the training set do? #
		for possession in train_set:
			label = 1 if possession.play_id == PLAY_TO_TEST else 0
			window_possessions = windowPositionsFromGetPositions(possession.positions,2,.5)
			final_label = 0
			instances = []
			for positions in window_possessions:
				vector = buildVector(positions,TIMES,False)
				guess = list(clf.predict(vector))[0]
				instances.append((positions['play_start'],positions['play_end'],guess))
				final_label = 1 if (guess or final_label == 1) else 0
			training_confusion[(1 if label==1 else 0)][(1 if final_label==1 else 0)] += 1

		# Test the holdout set #
		pos_in_set = 0
		for possession in test_set:
			label = 1 if possession.play_id == PLAY_TO_TEST else 0
			pos_in_set += label
			window_possessions = windowPositionsFromGetPositions(possession.positions,2,.5)
			final_label = 0
			instances = []
			for positions in window_possessions:
				vector = buildVector(positions,TIMES,False)
				guess = list(clf.predict(vector))[0]
				instances.append(guess)
				final_label = 1 if (guess or final_label == 1) else 0
			# if not (final_label == 0 and label == 0):
			# 		print '\n'
			# 		print possession.id
			# 		print 'Predicted Label: '+str(final_label)
			# 		print 'Actual Label: '+str(label)
			# 		print instances
			confusion[(1 if label== 1 else 0)][(1 if final_label==1 else 0)] += 1
			correct += 1 if label==final_label else 0
			total += 1
	print pass_1
	print pass_2
	print set(grr)
	# Print Out All The Final Scores
 	print '-------------------------------'
 	print 'Training Confusion Matrix'
 	ml.prettyPrintConfusionMatrix(training_confusion,[0,1])
 	print 'Actual Confusion Matrix'
 	ml.prettyPrintConfusionMatrix(confusion,[0,1])
 	print 'Final Score: '+str(float(correct)/total)
 	print '\n'
 	return float(correct)/total


########### This is multiclass scoring of the windowed method with OVA ##############
def scoreMultiClassWindowedML(basePositions,skf):
 	labels = list(set([possession.play_id for possession in basePositions if possession.play_id != 501])) # List of unique play IDs

 	results = [] # Stores the results in the form of tuples (guess,actual_label)

	for train_index,test_index in skf:
		# 1. Generate training and test sets
		train_set = retrieveIndexes(basePositions,list(train_index))
		test_set = retrieveIndexes(basePositions,list(test_index))
		
		# 2. Generate empty dictionaries to store training SVMs, positives stored as 1, negatives as 0
		svm_dictionary = {}
		for label in labels:
			length = LENGTHS[label] # How long is this play?
			# Generate the training vectors
			training_vectors = []
			for possession in train_set:
				play_id = possession.play_id
				if play_id == label:
					start_time = MANUAL_TIMES[label][possession.id] #The start time from manual recordings
					training_vectors.append((convertgetPositionToCustomTime(possession.positions,start_time,start_time-length),1,length,possession.id))
				else:
					window_possessions = windowPositionsFromGetPositions(possession.positions,length,.5)
					for positions in window_possessions:
						training_vectors.append((positions,0,length,possession.id))
			# Convert the training vectors into machine learning format
			ml_vectors = []
			ml_labels = []
			for positions,play_label,length,id in training_vectors:
				vector = buildVector(positions,timeListFromPlayLength(length),False)
				ml_vectors.append(vector)
				ml_labels.append(play_label)

			# Run the machine learning algorithms
			clf = svm.SVC(C=.3,class_weight={1:1,0:1},kernel='linear',probability=True)
			clf.fit(ml_vectors, ml_labels)
			svm_dictionary[label] = clf #Store the fitted SVM in the dictionary

		# 3. Test the holdout set
		for possession in test_set:
			# Run each test point through each SVM
			positive = [] # Track any positives
			for key,clf in svm_dictionary.items():
				play_length = LENGTHS[key]
				window_possessions = windowPositionsFromGetPositions(possession.positions,play_length,1)
				final_guess = 0
				high_probability = 0
				for poss in window_possessions:
					vector = buildVector(poss,timeListFromPlayLength(play_length),False)
					guess = list(clf.predict(vector))[0]
					probability = clf.predict_proba(vector)[0][0]
					if guess == 1:
						if final_guess == 0 or high_probability < probability:
							final_guess = 1
							high_probability = probability
				if final_guess == 1:
					positive.append((probability,key))
			# Look at all the positives and probabilities, to determine the ultimate guess
			ultimate_guess = 501 if not positive else max(positive)[1]
			
			# Store the Actual and the Guess
			results.append((ultimate_guess,possession.play_id))
	print 'Results Windowed Algorithm'
	return resultGeneration(results)

############# Takes list of tuples (guess,actual) and generates F scores and confusion matrices ##########
def resultGeneration(list_of_results):
	## Print Correct Classification Rate
	score = sum([(1 if label==guess else 0) for guess,label in list_of_results])/float(len(list_of_results))
	print 'Correct Classification Rate: '+str(round(score,2))
	# Compute the score
	labels = sorted(list(set([label for guess,label in list_of_results])))
	cm = [[0]*len(labels) for lb in range(len(labels))]
	counter = 0
	for result in list_of_results:
		guess = labels.index(result[0])
		actual = labels.index(result[1])
		cm[actual][guess] += 1
	plays = [PLAYS[label] for label in labels]
	x = PrettyTable(['']+plays)
	for i in range(len(cm)):
		x.add_row([PLAYS[labels[i]]]+cm[i])
	print x
############# generate time vector based on the length of the play ##########
def timeListFromPlayLength(length):
	return [i for i in range(length+1)]

########### Constructs the vectors used in the algorithms ##############
def buildVector(positions,TIMES,printed):
	bv = buildUniqueMeasureVectors(positions,TIMES)+buildSequenceClosenessVectors(positions,TIMES)+buildPositionVectors(positions,TIMES)+buildPassVectors(positions,TIMES,False)
	#bv = buildPassVectors(positions,TIMES,printed)
	#bv = buildUniqueMeasureVectors(positions,TIMES)+buildPassVectors(positions,TIMES,False)
	return bv

#####################################
####### Play Subset (Postup) ########
#####################################
def subsetRunGridSearch(basePositions):
	# Grid Search Criteria
	C_array = [5]
	class_weights = [3]
	max_score = 0
	scores = []
	for C in C_array:
		row = []
		for class_weight in class_weights:
			score = subsetRun(basePositions,C,class_weight)
			max_score = max(max_score,score)
			row.append(round(score,2))
		scores.append(row)
	print 'Grid Search: X-Axis is C-Array, Y-Axis is Positive_Class_Weight'
	ml.prettyPrintGrid(C_array,class_weights,scores)
	print 'Max Score: '+str(round(max_score,2))


######## Generates sliding window position objects #############
## Look same as full length but only for the specified amount of time
def windowPositionsFromGetPositions(getPositionResult,length,windowsize):
	play = getPositionResult
	windows = generatePlayWindows(play['play_start'],play['play_end'],length,windowsize)
	new_plays = []
	for window in windows:
		start = window[0]
		end = window[1]
		new_plays.append(convertgetPositionToCustomTime(play,start,end))
	return new_plays

##### Converts a full possession into a possession that fits within the window #####
def convertgetPositionToCustomTime(play_obj,start,end):
	play = play_obj.copy()
	# 1. Filter out easy_positions
	easy_positions = play['easy_positions']
	new_easy_positions = []
	for ep in easy_positions:
		if ep['time'] >= end and ep['time'] <= start:
			new_easy_positions.append(ep)
	play['easy_positions'] = new_easy_positions
	
	# 2. Filter out events
	new_events = []
	for event in play['events']:
		if event.clock >= end and event.clock <= start:
			new_events.append(event)
	play['events'] = new_events

	# 3. Filter out Positions
	new_positions = []
	for position in new_positions:
		if position.time_on_clock >= end and position.time_on_clock <= start:
			new_positions.append(position)
	play['positions'] = new_positions
	
	#4. Remaining labels
	play['play_start'] = start
	play['play_end'] = end
	return play

# Generates tuples of time windows given a start time, end time, window length, and slider length #
def generatePlayWindows(start_time,end_time,window_length,slider_length):
	total_length = start_time - end_time
	windows = []
	last_start = start_time
	while True:
		if last_start-window_length < end_time:
			break
		else:
			windows.append((last_start,last_start-window_length))
			last_start = last_start-slider_length
	return windows

## Takes in a list and an index list, and returns the list containing only elements that have indexes found
## in the index list. This is used to separate training and test data
def retrieveIndexes(list,indexes):
	new_list = []
	for index,itm in enumerate(list):
		if index in indexes:
			new_list.append(itm)
	return new_list


#####################################
####### Vector Construction #########
#####################################

###########################################################################
######### Functions to get player positions throughout the possession #####
###########################################################################

# Gets relevant positions from a possession
# Uses the second after everyone crosses half court and runs for POSS_LENGTH
def getPositions(possession):
	POSS_LENGTH = 8
	positions = Position.objects.filter(game_id=possession.game_number,
			quarter=possession.period,
			time_on_clock__lt=possession.time_start,
			time_on_clock__gt=possession.time_end
		).order_by("time_on_clock").reverse()
	# Find average position at the end of the possession
	last_position = positions[max(1,len(positions)-25)] # Take positions the second before the end of the possession to determine direction of the play
	average_x = sum([p[0] for p in easyPosition(last_position,False)['team_positions']])/5.0
	far_side_of_court = True if average_x > 47 else False
	# Find when the play starts
	play_start = None
	for position in positions:
		over_half_court = True
		for player in easyPosition(position,False)['team_positions']:
			if (not far_side_of_court and player[0] >= 47) or (far_side_of_court and player[0]<47):
				over_half_court = False
		if over_half_court:
			play_start = position.time_on_clock-.5
			break		
	# Play end is greater of POSS_LENGTH or 1 second before end of possession
	play_end = max(play_start-POSS_LENGTH,last_position.time_on_clock)
	positions = positions.filter(time_on_clock__lt=float(play_start),time_on_clock__gt=float(play_end))
	positions = uniquePositions(positions)
	easy_positions=[]
	for pos in positions:
		easy_positions.append(easyPosition(pos,far_side_of_court))

	# Get all the associated events as well with a possession
	events = Event.objects.filter(game_id=possession.game_number,
		quarter=possession.period,
		clock__lt=possession.time_start,
		clock__gt=possession.time_end
	).order_by("clock").reverse()
	dic = {'easy_positions':easy_positions,'far_side_of_court':far_side_of_court,'play_start':play_start,'play_end':play_end,'positions':positions,'events':events}
	return {'easy_positions':easy_positions,'far_side_of_court':far_side_of_court,'play_start':play_start,'play_end':play_end,'positions':positions,'events':events,'id':possession.id}


### A dictionary with normalized positions (to adjust for near or far side of the court) as well as ball and time information ###
def easyPosition(position,flipped):
	team_one_positions = [(position.team_one_player_one_x,position.team_one_player_one_y),(position.team_one_player_two_x,position.team_one_player_two_y),(position.team_one_player_three_x,position.team_one_player_three_y),(position.team_one_player_four_x,position.team_one_player_four_y),(position.team_one_player_five_x,position.team_one_player_five_y)]
	team_two_positions = [(position.team_two_player_one_x,position.team_two_player_one_y),(position.team_two_player_two_x,position.team_two_player_two_y),(position.team_two_player_three_x,position.team_two_player_three_y),(position.team_two_player_four_x,position.team_two_player_four_y),(position.team_two_player_five_x,position.team_two_player_five_y)]
	ball = [(position.ball_x,position.ball_y)]
	if position.team_one_id == 2:
		team_positions = team_one_positions
		defense_positions = team_two_positions
	else:
		team_positions = team_two_positions
		defense_positions = team_one_positions
	if flipped:
		for data in [team_positions,ball]:
			for tuples in range(len(data)):
				data[tuples] = (90-data[tuples][0],50-data[tuples][1])
	return {'team_positions':team_positions,'defense_positions':defense_positions,'ball':ball[0],'time':position.time_on_clock}

### Filters out any times that have more than one instance ###
def uniquePositions(position_objects):
	unique_times = []
	unique_positions = []
	for position in position_objects:
		if position.time_on_clock not in unique_times:
			unique_times.append(position.time_on_clock)
			unique_positions.append(position)
	return unique_positions


###########################################################################
######################## Build Pass Vectors ###############################
###########################################################################

def buildPassVectors(possession_obj,TIMES,printed):
	# Relevant Event IDs are as follows: 21:Dribble, 22:Pass, 23:Possession
	play_start = possession_obj['play_start']
	play_end = possession_obj['play_end']
	poss_length = play_start-play_end
	events = possession_obj['events']
	### Iterate through every event in the possession, generate a list of pass objects ###
	passes = []
	last_event = None
	for index,event in enumerate(events):
		if event.eventid == 22 and event.clock < play_start and event.clock > play_end:
			original_time = (last_event.clock if last_event else event.clock+.25)
			try:
				next_event = events[index+1]
			except:
				next_event = None
			final_time = (next_event.clock if next_event else event.clock-.25)
			original_ball_position = getPassMetrics(possession_obj,original_time)
			final_ball_position = getPassMetrics(possession_obj,final_time)
			closer_player = closerPlayer(final_ball_position,printed)
			distance = measure(original_ball_position['ball'],final_ball_position['ball'])['distance']
			up = True if original_ball_position['ball'][0]-final_ball_position['ball'][0] < 0 else False
			right = True if original_ball_position['ball'][1]-final_ball_position['ball'][1] < 0 else False
			time_into_play = play_start-event.clock
			#print 'Time: '+str(event.clock)+' Start: '+str(original_ball_position['ball'])+" End: "+str(final_ball_position['ball'])
			passes.append({'distance':distance,'start':original_ball_position['ball'],'end':final_ball_position['ball'],'time_into_play':time_into_play,'time':event.clock,'up':up,'right':right,'closer_player':closer_player})
	### Build the vectors from the pass objects ###
	times = generateTimesArray(TIMES,play_start,play_end)
	#pass_array = [0,0,0,0]*len(times)
	pass_array = [0,0,0,0,0,0]
	for index,passe in enumerate(passes):
		## Two options: just go chronologically, or you can also do it in time segments (I chose time segments) ##
		pass_type = passType(passe,printed)
		for index,time in enumerate(times):
			pass_time = passe['time'] 
			if pass_time >= time:
				#pass_array[index*4+pass_type] += 1
				pass_array[pass_type] += 1
				break
	return pass_array

### Checks if there is a player closer to the rim and on the same side of the court ###
# Takes in a single possession instance
def closerPlayer(possession_instance,printed):
	pi = possession_instance
	team_positions = pi['team_positions']
	posting_player = None
	posting_player_distance = 10000
	for player in team_positions:
		if measure(player,pi['ball'])['distance'] < posting_player_distance:
			posting_player = player
			posting_player_distance = measure(player,pi['ball'])['distance']
	# Check if any players are closer and on the same side of the court
	closer_player = False
	cp_obj = None
	for player in team_positions:
		same_side = True if ((player[1] < 25 and posting_player[1] < 25) or (player[1] > 25 and posting_player[1] > 25)) else False
		closer = True if (measure(player,(5,25))['distance']+2 < measure(posting_player,(5,25))['distance']) else False
		if same_side and closer:
			closer_player = True
			cp_obj = player
	next_closest_player_distance = sorted([measure(posting_player,tp)['distance'] for tp in team_positions])[1]
	player_nearby = True if next_closest_player_distance < 10 else False
	if printed:
		print 'posting_player'+str(posting_player)
		print 'closer_player'+str(cp_obj)
	return (closer_player or player_nearby)

def getPassMetrics(possession_obj,time):
	closest_instance = None
	delta = None
	easy_positions = possession_obj['easy_positions']
	for easy_position in easy_positions:
		if not delta or abs(easy_position['time']-time) < delta:
			delta = abs(easy_position['time']-time)
			closest_instance = easy_position
	return closest_instance

### Determine the pass type based on start and end positions ###
def passType(passe,printed):
	############# Updated Pass Types, to include 6 types of passes
	# (0) Interior, (1) Handoff, (2) Corner, (3) Entry, (4) Back Pass, (5) Other
	INTERIOR_THRESHOLD = 12 # feet from rim
	BASKET_POINT = (5.25,25)
	HANDOFF_THRESHOLD = 5 # total pass distance is less than X feet
	start_distance = measure(passe['start'],BASKET_POINT)['distance']
	end_distance = measure(passe['end'],BASKET_POINT)['distance']
	intercepts = interceptsFromTwoPoints(passe['start'],passe['end'])
	if printed:
		print passe
		print 'start_distance: '+str(start_distance)
		print 'end_distance: '+str(end_distance)
		print 'intercepts: '+str(intercepts)
	# Is it an interior pass?
	if start_distance < INTERIOR_THRESHOLD and end_distance < INTERIOR_THRESHOLD:
		return 0
	# Is it a handoff?
	elif passe['distance'] < HANDOFF_THRESHOLD:
		return 1
	# Is it a corner pass?
	elif (passe['end'][1] < 8 or passe['end'][1] > 42) and passe['end'][0] < 20:
		return 2
	# Is it an entry pass?
	elif end_distance < INTERIOR_THRESHOLD+7 and intercepts['y'] > -3 and intercepts['y'] < 53 and not passe['closer_player']:
		return 3
	# Did the pass go backwards?
	elif passe['end'][0] > passe['start'][0]:
		return 4
	# Must be a high entry then 
	else:
		return 5

### Returns the X and Y intercepts, given two points ###
def interceptsFromTwoPoints(point_one,point_two):
	p1x,p1y,p2x,p2y = float(point_one[0]),float(point_one[1]),float(point_two[0]),float(point_two[1])
	Y = p2y
	X = p2x
	p2x = p2x+.0001 if p2x==p1x else p2x
	m = ((p2y-p1y)/(p2x-p1x))
	b = Y - m*X
	x_intercept = -1*b/m
	return {'x':x_intercept,'y':b}


#***********************************************************************#
#***** Takes snapshots at given times in the possession and counts *****#
#***** number of players in each region of the court *******************#
#***********************************************************************#

def buildPositionVectors(easy_positions,TIMES):
	play_start = easy_positions['play_start']
	play_end = easy_positions['play_end']
	poss_length = play_start-play_end
	times = generateTimesArray(TIMES,play_start,play_end)
	positions = [[0]*25]*len(times)
	tracker = 0
	for easy_position in easy_positions['easy_positions']:
		if times[tracker]+.1 >= easy_position['time']:
			features = generatePositionVector(easy_position)
			positions[tracker] = features
			tracker += 1
		if tracker == len(times):
			break
	vector_positions = []
	for pos in positions:
		for p in pos:
			vector_positions.append(p)
	return vector_positions

### Generates a 2d vector that has counts for player positions in the possession ###
def generatePositionVector(easy_position):
	#average_positions = averagePositionOverTime(easy_positions)
	number_boxes = 5
	box_width = 10
	features = [0]*((number_boxes**2))
	for objs in easy_position['team_positions']:
		x_value = min(number_boxes-1,int(round(float(objs[0])/box_width)))
		y_value = min(number_boxes-1,int(round(float(objs[1])/box_width)))
		index = ((x_value)*number_boxes)+y_value
		features[index] += 1
	return features

### Returns a list of tuples with the average positions of each player from a list of easy_positions ###
def averagePositionOverTime(easy_positions):
	count = len(easy_positions)
	sum_x = [0]*5
	sum_y = [0]*5
	for easy_position in easy_positions:
		team_positions = easy_position['team_positions']
		for player_index in range(len(team_positions)):
			sum_x[player_index] += team_positions[player_index][0]
			sum_y[player_index] += team_positions[player_index][1]
	average_positions = [(sum_x[index]/count,sum_y[index]/count) for index in range(5)]
	return average_positions

#***********************************************************************#
#**************** Number on ball side in the possession ****************#
#***********************************************************************#

def buildUniqueMeasureVectors(easy_positions,TIMES):
	play_start = easy_positions['play_start']
	play_end = easy_positions['play_end']
	poss_length = play_start-play_end
	times = generateTimesArray(TIMES,play_start,play_end)
	ballside,inside = [0]*len(times), [0]*len(times)
	tracker = 0
	for easy_position in easy_positions['easy_positions']:
		if times[tracker]+.1 >= easy_position['time']:
			ballside[tracker] = numberOfBallSidePlayers(easy_position)
			inside[tracker] = playersInside(easy_position)
			tracker += 1
		if tracker == len(times):
			break
	return ballside+inside

### Number of players on the same side as the ball
def numberOfBallSidePlayers(easy_position):
	top_side = 0
	for tp in easy_position['team_positions']:
		if tp[1] < 25:
			top_side += 1
	ball_top_side = True if easy_position['ball'][1] < 25 else False
	return top_side if ball_top_side else (5-top_side)

### Number of players within 18 feet of the basket
def playersInside(easy_position):
	players_inside = 0
	for players in easy_position['team_positions']:
		distance = locationInAngleAndDistance(players)[0]
		if distance < 18:
			players_inside += 1
	return players_inside

#***********************************************************************#
#**************** Closness Instances  **********************************#
#***********************************************************************#

### Build feature vector from the closeness algorithm using a box algorithm ###
def buildClosenessVectors(possession_obj):
	easy_positions = possession_obj['easy_positions']
	closeness_obj = closeness(easy_positions)
	number_boxes = 5
	box_width = 10
	features = [0]*(((number_boxes**2))+1)
	for objs in closeness_obj:
		midpoint = objs['object'][2]
		x_value = min(number_boxes-1,int(round(float(midpoint[0])/box_width)))
		y_value = min(number_boxes-1,int(round(float(midpoint[1])/box_width)))
		index = (x_value*number_boxes)+y_value
		if objs['on_ball']: # Use a single counter for on ball screens
			features[-1] += 1
		features[index] += 1
	return features

########################
### Sequences Closeness Vectoors Categorizes the closeness over the time of the possession
### Types of positions: inside, outside, side or top?
def buildSequenceClosenessVectors(possession_obj,TIMES):
	easy_positions = possession_obj['easy_positions']
	closeness_obj = closeness(easy_positions)
	play_start = possession_obj['play_start']
	play_end = possession_obj['play_end']
	times = generateTimesArray(TIMES,play_start,play_end)
	vector = [0,0,0,0,0,0]*len(times)
	for objs in closeness_obj:
		midpoint = objs['object'][2]
		position = locationInAngleAndDistance(midpoint)
		inside = 1 if position[0] < 20 else 0
		#Court Degrees: 0-60:0, 60-120: 1,120-180:2
		court_degrees = (2 if position[1] < 60 else (1 if position[1] < 120  else 0))
		for idx in range(len(times)):
			time = times[idx]
			closeness_time = (objs['start']+objs['end'])/2.0
			if closeness_time >= time:
				vector[idx*6+(inside*court_degrees)] += 1
				break
	return vector

def closeness(easy_positions):
	THRESHOLD = 6
	# Get the distance array
	final_instances = []
	# Iterate through every combination of players
	for p1 in range(1,6):
		for p2 in range(p1+1,6):
				objs = findClosenssInstances(p1,p2,easy_positions,THRESHOLD)
				for obj in objs:
					final_instances.append(obj)
	return final_instances

# Finds instances where players get close together
def findClosenssInstances(player_no_1,player_no_2,easy_positions,THRESHOLD):
	# Filters all distances in the position to only those where the two players were close together
	distances = []
	for position in easy_positions:
		team_position = position['team_positions']
		dist = measure(team_position[player_no_1-1],team_position[player_no_2-1])
		if dist['distance'] < THRESHOLD:
			# Distance format: (time,min_distance,(Halfway_x,Halfway_y),(BallPos_X,BallPos_Y),player_1,player_2)
			distances.append((position['time'],dist['distance'],dist['halfway'],position['ball'],team_position[player_no_1-1],team_position[player_no_2-1]))
	
	# Group distance objects into larger instances of coming together, stored in instances
	instances = []
	temp_array = []
	for d in range(len(distances)-1):
		current = distances[d]
		next = distances[d+1]
		if current[0]-next[0] <= .12: # Threshold is 3x to avoid a player moving outside the threshold for a single frame then coming back, and counting that as two separate instances
			temp_array.append(current)
		else:
			instances.append(temp_array)
			temp_array = []
	if temp_array: # Don't forget to add the last one
		instances.append(temp_array)

	# Extract details from instances, including the min distance, length, boolean if on ball, etc. 
	objs = []
	for instance in instances:
		if instance:
			min_distance = (None,10000)
			length = instance[0][0]-instance[-1][0]
			on_ball = False
			first_instance = instance[0]
			if measure(first_instance[3],first_instance[4])['distance'] < 3 or measure(first_instance[3],first_instance[5])['distance'] < 3:
				on_ball=True
			for inst in instance:
				if inst[1] < min_distance[1]:
				 	min_distance = inst
			if length > .2:
				dict = {'start':instance[0][0],'end':instance[-1][0],'on_ball':on_ball,'object':min_distance,'length':length,'player_1':player_no_1,'player_2':player_no_2}
				objs.append(dict)
	return objs


#***********************************************************************#
#**************** Miscelleanous Helper Functions ***********************#
#***********************************************************************#


# Distance and midpoint between two positions
def measure(p1,p2):
	p1x = p1[0]
	p1y = p1[1]
	p2x = p2[0]
	p2y = p2[1]
	x = (p1x-p2x)**2
	y = (p1y-p2y)**2
	halfway = ((p1x+p2x)/2,(p1y+p2y)/2)
	return {'distance':(x+y)**.5,'halfway':halfway}

## Distance from the hoop and radians in relation to the basket
def locationInAngleAndDistance(position):
	DEGREE_MINIMIZER = 5 # Need to optimize this variable
	# Flip position if on the wrong side of the court
	player_x,player_y = position
	if player_x < 48:
		abs_pos = (player_x,player_y)
	else:
		abs_pos = (90-player_x,50-player_y)

	# Convert to radians from basket and distance
	distance = (((abs_pos[0]-0)**2)+((abs_pos[1]-25.0)**2))**0.5
	angle_x_offset = float(25-abs_pos[1])
	angle_y_offset = float(abs_pos[0])
	degrees = math.atan(angle_y_offset/angle_x_offset)*(180/math.pi) if angle_x_offset else 90
	degrees = degrees+180 if degrees < 0 else degrees
	#degrees = degrees / DEGREE_MINIMIZER
	return (distance,degrees)

### Generates time arrays from a time list
def generateTimesArray(times_array,play_start,play_end):
	times = []
	for time in times_array:
		times.append(max(play_start-time,play_end))
	return times

#***********************************************************************#
#**************** F Score **********************************************#
#***********************************************************************#
# beta = 2 weights recall higher than precision
# beta = .5 weights precision more than recall
# Precision = True Positives / (True Positives and True Negatives)
# Recall = True Positives / (True Positives and False Negatives)
def fScore(beta,true_positive,false_negative,false_positive,true_negative):
	numerator = (1+(beta**2))*true_positive
	denominator = numerator+((beta**2)*false_negative)+false_positive
	return round(float(numerator)/denominator,2)


#***********************************************************************#
#**************** Degree Distance Breakdown ****************************#
#***********************************************************************#
# court_dic = {10:[60,90,120],20:[45,135],100:[60,90,120]}
# points = [(8,80),(14,94),(25,178)]
# output is a list of counts for each of the distances, so the example is [0,1,0,0,0,1,0,0,0,0,1]
def generateDegreeDistanceList(court_dic,points):
	dic_ranges = []
	for key,value in court_dic.items():
		for degree in value:
			dic_ranges.append([key,degree,0])
		dic_ranges.append([key,360,0])
	sorted_dic_ranges = sorted(dic_ranges)
	for point in points:
		unplaced = True
		idx = 0
		while unplaced:
			if sorted_dic_ranges[idx][0] > point[0] and sorted_dic_ranges[idx][1] > point[1]:
				sorted_dic_ranges[idx][2] += 1
				unplaced = False
			else:
				idx += 1
	#print sorted_dic_ranges
	return [sdc[2] for sdc in sorted_dic_ranges]

#***********************************************************************#
#**************** Tools For Finding Events *****************************#
#***********************************************************************#

def events(possession_id):
	possession = Possession.objects.get(id=possession_id)
	start = possession.time_start+2
	end = possession.time_end-2
	print start
	print end
	events = Event.objects.filter(game_id=possession.game_number,
		quarter=possession.period,
		clock__lt=possession.time_start+2,
		clock__gt=possession.time_end-2
	).order_by("clock").reverse()
	for event in events:
		print event

def passevents(possession_id):
	possession = Possession.objects.get(id=possession_id)
	positions = getPositions(possession)
	print buildPassVectors(positions,[0,1,2,3,4,5,6],True)


