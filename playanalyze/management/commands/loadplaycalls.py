from django.core.management.base import BaseCommand, CommandError
from playanalyze.models import *
from playanalyze.helper import *
#########################################################
##### Load a new CSV file ############
#########################################################

class Command(BaseCommand):
    
    help = 'Loads the events csv file into the database'
   
    def handle(self, *args, **options):
        a = CelticPlay.objects.all()
        a.delete()
        ins = open("playanalyze/fixtures/data/nba_plays_celtics.txt", "r" )
        count = 0
        for line in ins:
            if not line.startswith("#"):
                line = line.replace("\n","")
                data = line.split(",")
                count += 1
                try:
                    play = CelticPlay(
                    game_id=int(data[0]),
                    quarter=int(data[9]),
                    start_game_clock=int(float(data[10])),
                    end_game_clock=int(float(data[6])),
                    parent_play=data[1],
                    play_name=data[2],
                    play_id=data[3],
                    home_team=data[4],
                    away_team=data[5],
                    wall_clock=data[7],
                    )
                    play.save()
                except Exception,e: 
                    print data
                    write(self,e)
                    #write(self,"Error at line "+str(count))
                    i =1
            if count % 1000 == 0:
                print count
        ins.close()
def write(self,string):
    self.stdout.write(str(string))
    return
