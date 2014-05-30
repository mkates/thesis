from playanalyze.models import *
import math

####### Given a celtic play, it figures out the most likely possession from the database
def mostLikelyPlay(celticplay):
	POTENTIAL_PLAYS = Possession.objects.filter(game_number=celticplay.game_id,period=celticplay.quarter)
	bestmatch = None
	percent_match = 0
	for play in POTENTIAL_PLAYS:
		po = percentOverlap(celticplay.start_game_clock,celticplay.end_game_clock,play.time_start,play.time_end)
		if po > percent_match:
			percent_match = po
			bestmatch = play
	if bestmatch:
		bestmatch.play = celticplay
		bestmatch.save()
	return

##### Helper to measure the percent overlap between two plays
def percentOverlap(start1,end1,start2,end2):
	length = int(start1-end1)
	if length == 0:
		return 0
	count = 0
	for time in range(int(math.floor(end1)),int(math.ceil(start1))):
		if time <= start2 and time >= end2:
			count += 1
	return count/float(length)

#### Converts game clock reading (11:23) to an integer 680
def gameClockToInteger(gameclock):
	clock = gameclock.split(":")
	return int(clock[0])*60+int(clock[1])
