
import json

loaded_config = None
player_config = None

def init_config():

	global loaded_config
	global player_config

	with open("config.json") as  fp:
		loaded_config = json.load(fp)

	with open("player_config.json") as fp:
		player_config = json.load(fp)


def get_config():

	global loaded_config
	return loaded_config

def get_player_config():

	global player_config
	return player_config
