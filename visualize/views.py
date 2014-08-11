from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from playanalyze.models import *
from playanalyze.helper import *
from playanalyze.analyze import *
from visualize.models import *
import json
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist


TEAM_KEY = {1:'Atlanta',
			2:'Boston',
			3:'New Orleans',
			4:'Chicago',
			5:'Cleveland',
			6:'Dallas',
			7:'Denver',
			8:'Detroit',
			9:'Golden State',
			10:'Houston', 
			11:'Indiana', 
			12:'Los Angeles Clippers', 
			13:'Los Angeles Lakers',
			14:'Miami',
			15:'Milwaukee',
			16:'Minnesota',
			17:'New Jersey',
			18:'New York',
			19:'Orlando',
			20:'Philadelphia',
			21:'Phoenix', 
			22:'Portland', 
			23:'Sacramento', 
			24:'San Antonio',
			25:'Oklahoma City',
			26:'Utah',
			27:'Washington', 
			28:'Toronto',
			29:'Memphis', 
			30:'Charlotte'}

@login_required
def visual(request):
	possessions = Possession.objects.exclude(play=None).order_by('id')
	#possessions = []
	# Get counts of each play
	counts = {}
	for poss in possessions:
		poss.play_name = poss.play.play_name
		if poss.play.play_name not in counts:
			counts[poss.play.play_name] = 1
		else:
			counts[poss.play.play_name] = counts[poss.play.play_name] + 1
	counts = sorted(counts.items(),key=lambda x:x[1],reverse=True)
	return render_to_response('index.html',{'possession_names':counts,'possessions':possessions},context_instance=RequestContext(request))

@login_required
def loadpossession(request):
	if request.method == 'GET':
		_type = request.GET.get('type','possession')
		_id = request.GET.get('id',0)
	try:
		possession = Possession.objects.get(id=_id)
	except:
		return HttpResponse(json.dumps({'status':501}), content_type='application/json')
	positions = getPositions(possession)
	data = createVisualData(possession,positions)
	return HttpResponse(json.dumps({'status':200,'play_array':data['play_array'],'closeness':closeness(positions['easy_positions']),'meta_data':data['meta_data']}), content_type='application/json')

def createVisualData(possession,getpositions):
	for event in getpositions['events']:
		print event
	play_array = []
	flipped = getpositions['far_side_of_court']
	positions = getpositions['positions']
	pos_o = positions[0]
	home = True if positions[0].team_one_id == 2 else False
	meta_data = {'game_id':possession.game_number,
		'team_one':TEAM_KEY[int(positions[0].team_one_id)],
		'team_two':TEAM_KEY[int(positions[0].team_two_id)],
		'quarter':possession.period,
		'possession_id':possession.id,
		'possession_name':possession.play.play_name
	}
	for pos in positions:
		pos_one = [pos.team_one_player_one_id,
			flippedX(flipped,pos.team_one_player_one_x),
			flippedY(flipped,pos.team_one_player_one_y),
			pos.team_one_player_two_id,
			flippedX(flipped,pos.team_one_player_two_x),
			flippedY(flipped,pos.team_one_player_two_y),
			pos.team_one_player_three_id,
			flippedX(flipped,pos.team_one_player_three_x),
			flippedY(flipped,pos.team_one_player_three_y),
			pos.team_one_player_four_id,
			flippedX(flipped,pos.team_one_player_four_x),
			flippedY(flipped,pos.team_one_player_four_y),
			pos.team_one_player_five_id,
			flippedX(flipped,pos.team_one_player_five_x),
			flippedY(flipped,pos.team_one_player_five_y)]
		pos_two = [pos.team_two_player_one_id,
			flippedX(flipped,pos.team_two_player_one_x),
			flippedY(flipped,pos.team_two_player_one_y),
			pos.team_two_player_two_id,
			flippedX(flipped,pos.team_two_player_two_x),
			flippedY(flipped,pos.team_two_player_two_y),
			pos.team_two_player_three_id,
			flippedX(flipped,pos.team_two_player_three_x),
			flippedY(flipped,pos.team_two_player_three_y),
			pos.team_two_player_four_id,
			flippedX(flipped,pos.team_two_player_four_x),
			flippedY(flipped,pos.team_two_player_four_y),
			pos.team_two_player_five_id,
			flippedX(flipped,pos.team_two_player_five_x),
			flippedY(flipped,pos.team_two_player_five_y)]
		combined = pos_one+pos_two if home else pos_two+pos_one
		play_array.append(combined+[flippedX(flipped,pos.ball_x),flippedY(flipped,pos.ball_y),pos.ball_z,pos.time_on_clock])
	return {'play_array':play_array,'meta_data':meta_data}

def flippedX(flipped,X):
	return X if not flipped else 90-X

def flippedY(flipped,Y):
	return Y if not flipped else 50-Y



