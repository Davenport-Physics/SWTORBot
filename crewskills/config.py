
import json

loaded_config = None

def init_config():

	global loaded_config

	with open("config.json") as  fp:
		loaded_config = json.load(fp)

def get_config():

	return loaded_config
