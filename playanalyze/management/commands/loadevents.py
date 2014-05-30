from django.core.management.base import BaseCommand, CommandError
from playanalyze.models import *
import playanalyze.views as views

#########################################################
##### Load a new CSV file ############
#########################################################

class Command(BaseCommand):
    
    help = 'Loads the events csv file into the database'
   
    def handle(self, *args, **options):
        e = Event.objects.all()
        e.delete()
        ins = open("playanalyze/fixtures/data/nba_events.csv", "r" )
        count = 0
        for line in ins:
            if not line.startswith("#"):
                line = line.replace("\n","")
                data = line.split(",")
                if not data[7]:
                    data[7] = -1
                count += 1
                try:
                    event = Event(
                    game_id=int(data[0]),
                    quarter=int(data[1]),
                    clock=float(data[2]),
                    eventid=int(data[3]),
                    time=data[4],
                    playerid=int(data[5]),
                    gplayerid=int(data[6]),
                    pbpseqnum=int(data[7])
                    )
                    event.save()
                except Exception,e: 
                    write(self,e)
                    i =1
            if count % 5000 == 0:
                print count
        ins.close()

def write(self,string):
    self.stdout.write(str(string))
    return
