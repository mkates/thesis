import json
import os

def parseCelticsPlays():
	ins = open( "celtics_play_calls.csv", "r" )
	out = open("celtics_play_calls.json",'w').close()
	out = open("celtics_play_calls.json",'w')
	out.write('[')
	array = []
	count = 1
	for line in ins:
		if not line.startswith('#'):
			a = line.split(",")
			a[6] = a[6].replace(":",".")
			try:
				dict = {"pk":count,"model":"classifyapp.celticsplay","fields":{"game_number":a[0],"parent_play":a[1],"play_name":a[2],"play_id":a[3],"home_team":a[4],"away_team":a[5],"game_clock":a[6],"wall_clock":a[7],"period":a[8]}}
				jsoned = json.dumps(dict)
				out.write(jsoned)
				out.write(",")
			except:
				print a
			count += 1
	out.seek(-1, os.SEEK_END)
	out.truncate()
	out.write("]")
	ins.close()
	out.close()

def extractGames():
	ins = open( "/users/alexanderkates/documents/Thesis/sportvu_data/nba_games.csv", "r" )
	array = []
	all_games = []
	for line in ins:
		if not line.startswith('#'):
			a = line.split(",")
			game_id = a[0]
			home_id = a[1]
			away_id = a[2]
			if (int(game_id) not in all_games):
				all_games.append(int(game_id))
			if (int(game_id) not in array) and (home_id=='2' or away_id=='2'):
				array.append(int(game_id))
	print len(array)
	print len(all_games)
	ins.close()

def extractPositions():
	ins = open("/users/alexanderkates/desktop/Position_Data_sample.csv", "r" )
	out = open("/users/alexanderkates/desktop/Position_Data_sample_out.csv", "w" ).close()
	out = open("/users/alexanderkates/desktop/Position_Data_sample_out.csv", "w" )
	global_counter = 0
	new_lines = 0
	time_on_clock = -1 # Dummy variable
	template = ['gameID','quarter','clock','time','team_1','team_2','offense_arrayx15','defense_arrayx15',
	'ballx3'] # Total Length:38
	temp_dict = [None]*39
	player_count = 0
	for line in ins:
		if not line.startswith('g'):
			variables = [float(x) for x in line.split(",")]
			if variables[4] == -2:
				if not None in temp_dict:
					new_lines += 1
					for integers in [0,1,3,4,5,6,9,12,15,18,21,24,27,30,33]:
						temp_dict[integers] = int(temp_dict[integers])
					out.write(str(temp_dict).replace(" ","").replace("[","").replace("]","")+"\n")
				player_count = 0
				temp_dict = [None]*39
			if not temp_dict[0] and temp_dict[4] != -2: # Set the meta information if not set
				temp_dict[0:4] = variables[0:4]
			if variables[4] == -1: # If its the ball
				temp_dict[36:39] = variables[6:9]
			elif variables[4] > 0: # If its a player
				if player_count == 0: #Set the offense team ID
					temp_dict[4] = variables[4]
				elif player_count == 5:
					temp_dict[5] = variables[4]
				#Set the team ids
				temp_dict[6+(player_count*3):9+(player_count*3)] = variables[5:8]
				player_count += 1
		global_counter += 1
		if global_counter % 50000 == 0:
			print global_counter
	# print global_counter
	print new_lines
	ins.close()
	out.close()

GAME_IDS = [2012121410, 2012012702, 2013011402, 2013011102, 2013010902, 2012021202, 2013011602, 2012111702, 2012122102, 2012033016, 2013050302, 2012122909, 2012121202, 2012020502, 2013020102, 2013042802, 2013022221, 2013042602, 2013010402, 2012011802, 2012010402, 2012041718, 2013021302, 2013011802, 2013040116, 2013012702, 2012121524, 2012020902, 2012012002, 2013013002, 2012110702, 2013031802, 2013030802, 2012112802, 2012120802, 2012021502, 2012041802, 2013031602, 2012110327, 2012032802, 2012060702, 2012020102, 2012011102, 2013042018, 2012032215, 2012030402, 2013020302, 2012112519, 2012022902, 2013033118, 2013021002, 2012112102, 2013032705, 2012032502, 2013031302, 2012010602, 2012052602, 2013020702, 2012052102, 2013030102, 2013050118, 2013020628, 2012112302, 2012010202, 2013040702, 2012030902, 2012031409, 2012111402, 2012030202, 2012040102, 2012041102, 2012020702, 2013032902, 2013032206, 2013041728, 2012011302, 2012121902, 2013031025, 2011123002, 2013042318, 2012040802, 2012060102, 2013012205, 2013012402, 2012021028, 2012040402, 2013030520, 2013041002, 2013041319, 2013032602, 2012120502, 2012113002, 2012012902, 2013010718, 2012041328, 2013010202, 2012111015, 2012110202, 2012110902, 2013040502, 2012120115, 2012060302, 2013040302, 2012030602, 2012012302, 2012020302]
def cleanPossessions():
	ins = open("data/nba_events.csv", "r" )
	out = open("data/nba_events_clean.csv", "w" ).close()
	out = open("data/nba_events_clean.csv", "w" )
	for line in ins:
		if not line.startswith('#'):
			a = line.split(",")
			if int(a[0]) in GAME_IDS:
				out.write(line)
	ins.close()
	out.close()

def match_games():
	ins = open("data/celtics_play_calls_2012_13.csv", "r" )
	table = open("data/celticgamid_to_sportvugameid.txt", "r" )
	out = open("data/celtic_play_calls_2012_13_2.csv", "w" ).close()
	out = open("data/celtic_play_calls_2012_13_2.csv", "w" )
	#out = open("data/celticgamid_to_sportvugameid.txt", "w" ).close()
	#out = open("data/celticgamid_to_sportvugameid.txt", "w" )
	game_ids = {}
	for line in table:
		if not line.startswith('#'):
			a = line.replace(" ","").split(",")
			print a
			try:
				int(a[2])
			except:
				game_ids[int(a[0])] = int(a[1])
	for bline in ins:
		if not bline.startswith('#'):
			a = bline.split(",")
			a.pop()
			a[0] = game_ids[int(a[0])]
			a = str(a)
			a = a.replace("[","").replace("]","").replace(" ","").replace("' ","")
			out.write(a+"\n")
	ins.close()
	table.close()
	out.close()

PLAY_GAME_IDS = [2012103015, 2012110202, 2012110327, 2012110702, 2012110902, 2012111015, 2012111204, 2012111402, 2012111517, 2012111702, 2012111808, 2012112102, 2012112302, 2012112519, 2012112802, 2012113002, 2012120115, 2012120502, 2012120720, 2012120802, 2012121202, 2012121410, 2012121524, 2012121804, 2012121902, 2012122102, 2012122517, 2012122712, 2012122909, 2012123023, 2013010202, 2013010402, 2013010501, 2013010718, 2013010902, 2013011102, 2013011402, 2013011602, 2013011802, 2013012008, 2013012205, 2013012402, 2013012501, 2013012702, 2013013002, 2013020102, 2013020302, 2013020628, 2013020702]
def getGame():
	ins = open("data/nba_positions.csv", "r" )
	out = open("data/nba_positions_min.csv", "w" ).close()
	out = open("data/nba_positions_min.csv", "w" )
	for line in ins:
		gameid = line[0:10]
		if int(gameid) in PLAY_GAME_IDS:
			out.write(line)
	ins.close()
	out.close()

def getCelticPlayGameIDS():
	ins = open("data/temp.txt", "r" )
	GAMES = []
	for line in ins:
		if not line.startswith('#'):
			a = line.split(',')[0]
			if int(a) not in GAMES:
				GAMES.append(int(a))
	print GAMES
	ins.close()

def fileCount(file_name):
	ins = open(file_name, "r" )
	count = 0
	for line in ins:
		count += 1
	print count
	ins.close()
fileCount('data/nba_positions_min.csv')


