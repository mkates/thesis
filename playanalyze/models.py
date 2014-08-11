from django.db import models
from playanalyze.play_start_and_end import *

########### Celtics Play Calls ############
class CelticPlay(models.Model):
	game_id = models.IntegerField(max_length = 9)
	quarter = models.IntegerField(max_length=1)
	start_game_clock = models.FloatField(max_length = 10)
	end_game_clock = models.FloatField(max_length=10)
	
	### Play Information ###
	# Parent Plays: SOB, BOB, transition, halfcourt
	parent_play = models.CharField(max_length=20)
	play_name = models.CharField(max_length=40)
	play_id = models.IntegerField(max_length=9)
	home_team = models.CharField(max_length=40)
	away_team = models.CharField(max_length=40)
	wall_clock = models.CharField(max_length = 10)

	### Does it have associated position and event data? ###
	data_available = models.BooleanField(default=False)

########### Position Object ############
class Position(models.Model):

	#Game Information
	game_id = models.BigIntegerField(max_length=13)
	quarter = models.IntegerField(max_length=1)
	time_on_clock = models.FloatField(max_length=3)
	time = models.BigIntegerField(max_length=13)
	
	#Team IDs
	team_one_id = models.IntegerField(max_length=2)
	team_two_id = models.IntegerField(max_length=2)
	
	#Offense positions
	team_one_player_one_id = models.BigIntegerField(max_length=13)
	team_one_player_one_x = models.FloatField(max_length=13)
	team_one_player_one_y = models.FloatField(max_length=13)
	team_one_player_two_id = models.BigIntegerField(max_length=13)
	team_one_player_two_x = models.FloatField(max_length=13)
	team_one_player_two_y = models.FloatField(max_length=13)
	team_one_player_three_id = models.BigIntegerField(max_length=13)
	team_one_player_three_x = models.FloatField(max_length=13)
	team_one_player_three_y = models.FloatField(max_length=13)
	team_one_player_four_id = models.BigIntegerField(max_length=13)
	team_one_player_four_x = models.FloatField(max_length=13)
	team_one_player_four_y = models.FloatField(max_length=13)
	team_one_player_five_id = models.BigIntegerField(max_length=13)
	team_one_player_five_x = models.FloatField(max_length=13)
	team_one_player_five_y = models.FloatField(max_length=13)
	
	#Defense positions
	team_two_player_one_id = models.BigIntegerField(max_length=13)
	team_two_player_one_x = models.FloatField(max_length=13)
	team_two_player_one_y = models.FloatField(max_length=13)
	team_two_player_two_id = models.BigIntegerField(max_length=13)
	team_two_player_two_x = models.FloatField(max_length=13)
	team_two_player_two_y = models.FloatField(max_length=13)
	team_two_player_three_id = models.BigIntegerField(max_length=13)
	team_two_player_three_x = models.FloatField(max_length=13)
	team_two_player_three_y = models.FloatField(max_length=13)
	team_two_player_four_id = models.BigIntegerField(max_length=13)
	team_two_player_four_x = models.FloatField(max_length=13)
	team_two_player_four_y = models.FloatField(max_length=13)
	team_two_player_five_id = models.BigIntegerField(max_length=13)
	team_two_player_five_x = models.FloatField(max_length=13)
	team_two_player_five_y = models.FloatField(max_length=13)
	
	# Ball Positions
	ball_x = models.FloatField(max_length=13)
	ball_y = models.FloatField(max_length=13)
	ball_z = models.FloatField(max_length=13)

	def __unicode__(self):
		return (self.ball_x,self.ball_y)

########### Events ############
class Event(models.Model):
	game_id = models.BigIntegerField(max_length=13)
	quarter = models.IntegerField(max_length=1)
	clock = models.FloatField(max_length=13)
	eventid = models.IntegerField(max_length=4)
	time = models.CharField(max_length=100)
	playerid = models.BigIntegerField(max_length=13)
	gplayerid = models.BigIntegerField(max_length=13)
	pbpseqnum = models.BigIntegerField(max_length=13)

	def event_name(self):
		EVENT_KEY = {1:'Free Throw Made',
			2:'Free Throw Missed',
			3:'Field Goal Made',
			4:'Field Goal Missed',
			5:'Offensive Rebound',
			6:'Defensive Rebound',
			7:'Turnover',
			8:'Foul',
			21:'Dribble',
			22:'Pass',
			23:'Possession',
			24:'Blocked Shot',
			25:'Assist'}
		return EVENT_KEY[self.eventid]

	def __unicode__(self):
		return "Game: "+str(self.game_id)+" Event: "+str(self.eventid)+", "+self.event_name()+" Clock: "+str(self.clock)

class Possession(models.Model):
	play = models.ForeignKey(CelticPlay,null=True,blank=True)
	game_number = models.IntegerField(max_length = 9)
	team = models.IntegerField(default=2)
	period = models.IntegerField(max_length=1)
	time_start = models.IntegerField(max_length = 3)
	time_end = models.IntegerField(max_length = 3)
	touches = models.IntegerField(max_length = 3)
	passes = models.IntegerField(max_length = 3)
	dribbles = models.IntegerField(max_length = 3)
	result = models.CharField(max_length = 20)
	points = models.IntegerField(max_length = 1)

	def length(self):
		return self.time_start-self.time_end

