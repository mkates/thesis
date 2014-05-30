from django.core.management.base import BaseCommand, CommandError
from playanalyze.helper import *
from playanalyze.models import *
#########################################################
# Match SportVu Possession to Celtic Play ###############
#########################################################

class Command(BaseCommand):
    def handle(self, *args, **options): 
		count = 0
		for cp in CelticPlay.objects.all():
			mostLikelyPlay(cp)
			count +=1
			if count % 10 == 0: