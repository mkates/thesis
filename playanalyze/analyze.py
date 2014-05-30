from playanalyze.models import *
from playanalyze.helper import *
import playanalyze.ml as ml
import math
import inspect as inspect
##########################################################
######### Hand Extracted Plays That Are Run Well #########
##########################################################

# PlayID: 32
# PUNCH = [128,320,987,2780,3187,4445,4596,5133,5581,5714]

ELBOW = [100,105,137,510,968,1200,1217,1218,1220,1223,2822,3394,3398,3426,3435,3438,3444,4118,4136,4180,4182,4184,4411,4417,4434,4479,4485,4579,4582,4609,4646,5148,5214,5451,5590,5592,5631,5637,5682,5706,5735,5855,6025,6201,6205,6251,6294,6299,6300,6312,6315,6317,6318,6334,6643,7004,7008,7080,7356,7366,7376,7385]

FLOPPY = [97,111,117,190,198,200,292,338,350,499,519,920,921,927,971,990,1213,1253,2751,2771,2787,3367,3401,3921,3942,3943,3944,3946,3983,3985,4003,4004,4120,4135,4145,4405,4412,4416,4423,4428,4433,4478,4603,5142,5196,5436,5649,5843,5871,6026,6043,6064,6264,6672,6673,6713,6998,7009,7026,7028,7355,7406,8771,8973,8999,9129,9237,9241,9281,9287,9453,9798,10085,10101]

HORNS = [181,182,183,184,185,1210,1211,1212,1243,1258,2826,4137,4138,4183,4488,5477,5737,5921,6094,6346,6347,7027,7077,8841,8845,9164,9196,9208,9213,9219,9786,10093]

#This is a tough play to differentiate
INVERT = [107, 334, 919, 1202, 1204, 1249, 3237, 3836, 3933, 3939, 4113, 4179, 4399, 4403, 4425, 4447, 4481, 4490, 4614, 4655, 5400, 5660, 5661, 5680, 5700, 5719, 5724, 5842, 6086, 6231, 7030, 8812, 9014, 9147, 9192, 9230, 9264, 10114, 10134]

DELAY = [118,215,323,1194,2749,2785,2788,3212,3236,3244,3853,3870,3906,3907,3908,3909,3920,3974,4006,4442,4634,4636,4654,5138,5139,5441,5617,5626,5627,5628,5712,5733,5888,5899,5912,5916,6080,6131,6134,6168,6182,6188,6268,6719,6999,7069,7071,7084,7400,7458,8564,8732,8770,8825,8826,8827,8969,8970,8971,8989,9163,9177,9211,9212,9258,9298,9302,9397,9398,9399,9400,9404,9486,9492,9493,9494,9527,9581,9875,10133]

PLAYS = {26:'ELBOW',42:'FLOPPY',53:'HORNS',98:'INVERT',92:'DELAY',32:'PUNCH'}

#####################################
######### Main Run Function #########
#####################################

def basePositions():
	plays = [ELBOW,FLOPPY]
	dic={'ELBOW':ELBOW,'FLOPPY':FLOPPY,'HORNS':HORNS,'INVERT':INVERT,'DELAY':DELAY}
	for key,value in dic.iteritems():
		relevant_possession_ids = value
		possessions = Possession.objects.filter(id__in=relevant_possession_ids)
		for possession in possessions:
			possession.positions = getPositions(possession)
		dic[key] = list(possessions)
		print str(key)+" complete"
	return dic

def run(basePositions):
	vectors = []
	results = []
	possessionids = []
	count = 0
	for possession in basePositions:
		play_id = possession.play.play_id
		if play_id in PLAYS.keys():
			#vector = buildUniqueMeasureVectors(possession.positions)+buildClosenessVectors(possession.positions)
			vector = buildUniqueMeasureVectors(possession.positions)
			vectors.append(vector)
			results.append(play_id)
			possessionids.append(possession.id)
		else: #Catch any plays that aren't in set, otherwise ML algorithm will break
			print 'WRONG PLAY: '+str(play_id)+" "+str(possession.id)
	ml.runAnalysis(vectors,results,possessionids)
	# for i in range(len(vectors)):
	# 	print str(vectors[i])+": "+str(results[i])
	print "\nVector Length: "+str(len(vector))
	print '\nANALYSIS COMPLETE'
	#return (vectors,results)

### Build feature vector from the closeness algorithm using a box algorithm ###
def buildClosenessVectors(possession_obj):
	easy_positions = possession_obj['easy_positions']
	closeness_obj = closeness(easy_positions)
	snapShotPositions = buildPositionVectors(possession_obj)
	number_boxes = 5
	box_width = 10
	features = [0]*(((number_boxes**2)*2)+1)
	for objs in closeness_obj:
		midpoint = objs['object'][2]
		x_value = int(round(float(midpoint[0])/box_width))
		y_value = int(round(float(midpoint[1])/box_width))
		index = (x_value*number_boxes)+y_value
		if objs['on_ball']: # Use a single counter for on ball screens
			features[-1] += 1
		features[index] += 1
	return features

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
			play_start = position.time_on_clock-1.0
			break		
	# Play end is greater of POSS_LENGTH or 1 second before end of possession
	play_end = max(play_start-POSS_LENGTH,last_position.time_on_clock)
	positions = positions.filter(time_on_clock__lt=float(play_start),time_on_clock__gt=float(play_end))
	positions = uniquePositions(positions)
	easy_positions=[]
	for pos in positions:
		easy_positions.append(easyPosition(pos,far_side_of_court))
	return {'easy_positions':easy_positions,'far_side_of_court':far_side_of_court,'play_start':play_start,'play_end':play_end,'positions':positions}



### A dictionary with normalized positions (to adjust for near or far side of the court) as well as ball and time information ###
def easyPosition(position,flipped):
	if position.team_one_id == 2: #If Celtics are the home team, they are team one
		team_positions = [(position.team_one_player_one_x,position.team_one_player_one_y),(position.team_one_player_two_x,position.team_one_player_two_y),(position.team_one_player_three_x,position.team_one_player_three_y),(position.team_one_player_four_x,position.team_one_player_four_y),(position.team_one_player_five_x,position.team_one_player_five_y)]
	else:
		team_positions = [(position.team_two_player_one_x,position.team_two_player_one_y),(position.team_two_player_two_x,position.team_two_player_two_y),(position.team_two_player_three_x,position.team_two_player_three_y),(position.team_two_player_four_x,position.team_two_player_four_y),(position.team_two_player_five_x,position.team_two_player_five_y)]
	ball = [(position.ball_x,position.ball_y)]
	if flipped:
		for data in [team_positions,ball]:
			for tuples in range(len(data)):
				data[tuples] = (90-data[tuples][0],50-data[tuples][1])
	return {'team_positions':team_positions,'ball':ball[0],'time':position.time_on_clock}

### Filters out any times that have more than one instance ###
def uniquePositions(position_objects):
	unique_times = []
	unique_positions = []
	for position in position_objects:
		if position.time_on_clock not in unique_times:
			unique_times.append(position.time_on_clock)
			unique_positions.append(position)
	return unique_positions


#***********************************************************************#
#***** Takes snapshots at given times in the possession and counts *****#
#***** number of players in each region of the court *******************#
#***********************************************************************#

def buildPositionVectors(easy_positions):
	play_start = easy_positions['play_start']
	play_end = easy_positions['play_end']
	poss_length = play_start-play_end
	snap_range_end = [play_start-(poss_length*.25),play_start-(poss_length*.5),play_start-(poss_length*.75)]
	groups = [[],[],[]]
	for easy_position in easy_positions['easy_positions']:
		if easy_position['time'] >= snap_range_end[0]:
			groups[0].append(easy_position)
		elif easy_position['time'] >= snap_range_end[1]:
			groups[1].append(easy_position)
		elif easy_position['time'] >= snap_range_end[2]:
			groups[2].append(easy_position)
	return generatePositionVector(groups[0])+generatePositionVector(groups[1])+generatePositionVector(groups[2])

### Generates a 2d vector that has counts for player positions in the possession ###
def generatePositionVector(easy_positions):
	average_positions = averagePositionOverTime(easy_positions)
	number_boxes = 3
	box_width = 15
	features = [0]*(((number_boxes**2)*2)+1)
	for objs in average_positions:
		x_value = int(round(float(objs[0])/box_width))
		y_value = int(round(float(objs[1])/box_width))
		index = (x_value*number_boxes)+y_value
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
def buildUniqueMeasureVectors(easy_positions):
	play_start = easy_positions['play_start']
	play_end = easy_positions['play_end']
	poss_length = play_start-play_end
	quantity = 4
	times = [play_start,max(play_start-2,play_end),max(play_start-4,play_end),max(play_start-6,play_end)]
	ballside,inside = [0]*quantity, [0]*quantity
	tracker = 0
	for easy_position in easy_positions['easy_positions']:
		if times[tracker]+.1 >= easy_position['time']:
			ballside[tracker] = numberOfBallSidePlayers(easy_position)
			inside[tracker] = playersInside(easy_position)
			tracker += 1
		if tracker == quantity:
			break
	pc = playersClose(easy_positions)
	return ballside+inside

def numberOfBallSidePlayers(easy_position):
	top_side = 0
	for tp in easy_position['team_positions']:
		if tp[1] < 25:
			top_side += 1
	ball_top_side = True if easy_position['ball'][1] < 25 else False
	return top_side if ball_top_side else (5-top_side)

def playersInside(easy_position):
	players_inside = 0
	for players in easy_position['team_positions']:
		distance = locationInAngleAndDistance(players)[0]
		if distance < 18:
			players_inside += 1
	return players_inside

def playersClose(easy_positions):
	inside,outside = 0,0
	on_ball = 0
	closeness_obj = closeness(easy_positions['easy_positions'])
	for close in closeness_obj:
		if close['start'] > easy_positions['play_start']-5:
			midpoint = close['object'][2]
			if close['on_ball']:
				on_ball+=1
			if locationInAngleAndDistance(midpoint)[0] < 17:
				inside+=1
			else:
				outside+=1
	return[inside,outside,on_ball]

#***********************************************************************#
##**** Find all the instances where players get close to each other ****#
#***********************************************************************#

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



