from django.core.management.base import BaseCommand, CommandError
from playanalyze.models import *
import playanalyze.views as views

#########################################################
##### Load a new CSV file ############
#########################################################

class Command(BaseCommand):
    
    help = 'Loads in the csv file into the database'
   
    def handle(self, *args, **options):
        a = Position.objects.all()
        a.delete()
        ins = open( "playanalyze/fixtures/data/nba_positions_min.csv", "r" )
        count = 0
        for line in ins:
            line = line.replace("\n","")
            data = line.split(",")
            count += 1
            try:
                position = Position(
                game_id = data[0],
                quarter = data[1],
                time_on_clock = data[2],
                time = data[3],
                team_one_id = data[4],
                team_two_id = data[5],
                team_one_player_one_id = data[6],
                team_one_player_one_x = data[7],
                team_one_player_one_y = data[8],
                team_one_player_two_id = data[9],
                team_one_player_two_x = data[10],
                team_one_player_two_y = data[11],
                team_one_player_three_id = data[12],
                team_one_player_three_x = data[13],
                team_one_player_three_y = data[14],
                team_one_player_four_id = data[15],
                team_one_player_four_x = data[16],
                team_one_player_four_y = data[17],
                team_one_player_five_id = data[18],
                team_one_player_five_x = data[19],
                team_one_player_five_y = data[20],
                team_two_player_one_id = data[21],
                team_two_player_one_x = data[22],
                team_two_player_one_y = data[23],
                team_two_player_two_id = data[24],
                team_two_player_two_x = data[25],
                team_two_player_two_y = data[26],
                team_two_player_three_id = data[27],
                team_two_player_three_x = data[28],
                team_two_player_three_y = data[29],
                team_two_player_four_id = data[30],
                team_two_player_four_x = data[31],
                team_two_player_four_y = data[32],
                team_two_player_five_id = data[33],
                team_two_player_five_x = data[34],
                team_two_player_five_y = data[35],
                ball_x = data[36],
                ball_y = data[37],
                ball_z = data[38])
                position.save()
                if count % 10000 == 0:
                    print count
            except Exception,e: 
                write(self,"Error at line "+str(count))
        ins.close()

def write(self,string):
    self.stdout.write(str(string))
    return
