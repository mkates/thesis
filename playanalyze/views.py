from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from playanalyze.models import *
from playanalyze.helper import *
from django.db.models import Q

########################################
##### Displaying the Data ##############
########################################

def celticplays(request):
	return render_to_response('celticplays.html',{'possession':Possession.objects.exclude(play=None)},context_instance=RequestContext(request))

def possessions(request):
	pandc = getPossessionCountsAndList()
	return render_to_response('possessions.html',{'counts':pandc['play_counts'],'play_list':pandc['play_list']},context_instance=RequestContext(request))

def run(request):
	return













































