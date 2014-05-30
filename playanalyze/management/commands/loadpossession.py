from django.core.management.base import BaseCommand, CommandError
from account.models import * 
from visualize.models import *
from playanalyze.models import *
from playanalyze.helper import *
#########################################################
##### Load a new CSV file ############
#########################################################

class Command(BaseCommand):
    
    help = 'Loads in the possessions / play calls'
   
    def handle(self, *args, **options):	
        p = Possession.objects.all()
        p.delete()
        ins = open("playanalyze/fixtures/data/nba_possessions.csv", "r" )
        count = 0
        for line in ins:
            if not line.startswith("#"):
                line = line.replace("\n","")
                data = line.split(",")
                count += 1
                try:
                    possession = Possession(
                    game_number=int(data[0]),
                    period=int(data[1]),
                    time_start=gameClockToInteger(data[5]),
                    time_end=gameClockToInteger(data[6]),
                    touches=data[8],
                    passes=data[9],
                    dribbles=data[10],
                    result=data[11],
                    points=data[12]
                    )
                    possession.save()
                except Exception,e: 
                    write(self,e)
                    #write(self,"Error at line "+str(count))
                    i =1
            if count % 5000 == 0:
                print count
        ins.close()







			
def write(self,string):
	self.stdout.write(str(string))
	return
