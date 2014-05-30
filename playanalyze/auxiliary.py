#########################################################
#### Auxiliary Functions Not To Clutter Up Analyze.py ###
#########################################################


### Finds all possessions that have more than 20 instances in the database ###
def getPossessionCountsAndList():
	# Only plays that have a label
	possessions = Possession.objects.exclude(play=None)
	# Get counts of each play
	counts = {}
	for poss in possessions:
		poss.play_name = poss.play.play_name
		if poss.play.play_name not in counts:
			counts[poss.play.play_name] = 1
		else:
			counts[poss.play.play_name] = counts[poss.play.play_name] + 1
	counts = sorted(counts.items(),key=lambda x:x[1],reverse=True)

	# Remove instances that don't have enough samples
	MIN_AMOUNT = 20
	eligible_play_counts = []
	for count in counts:
		if count[1] >= MIN_AMOUNT and count[0] != 'Random' and count[0] != 'Transition':
			eligible_play_counts.append(count)
	# Generate list of available plays
	play_list = [play[0] for play in eligible_play_counts]

	possession_objects = possessions.filter(play__play_name__in=play_list)
	return {'play_counts':eligible_play_counts,'play_list':play_list,'possession_objects':possession_objects}
	
### Calculates the location in angles and degrees of a position ###
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