from django.core.management.base import BaseCommand, CommandError

#########################################################
##### Analyzes a game ###################################
#########################################################
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

class Command(BaseCommand):
    
    help = 'Adds end times to each celtic play'
   
    def handle(self, *args, **options): 
		POSITION_ENDERS = [3,4,7,8]
		eventsall = Event.objects.all()
		for plays in CelticPlay.objects.filter(parent_play="Halfcourt"):
			# Find the event data for next 24 hours
			events = eventsall.filter(game_id=plays.game_id,quarter=plays.quarter,clock__range=[plays.end_game_clock,plays.start_game_clock])
			print ''
			print str(plays.game_id)+" "+str(plays.quarter)+" "+str(plays.start_game_clock)
			print plays.play_name
			print "Play Start: "+str(plays.start_game_clock)+ " Play End: "+str(plays.end_game_clock)+" Length: "+str(plays.start_game_clock-plays.end_game_clock)
			for event in events:
				print str(event.clock)+": "+str(EVENT_KEY[event.eventid])
def write(self,string):
    self.stdout.write(str(string))
    return
