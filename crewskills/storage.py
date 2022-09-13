
import sqlite3

con = None
cur = None

def init_database():

	global con
	global cur

	con = sqlite3.connect("crewskills.db")
	cur = con.cursor()
	with open("./sql/tables.sql", "r") as fp:
		sql_commands = fp.read()

	cur.executescript(sql_commands)
	con.commit()

def save_mission_details(mission):

	sql_command = """INSERT INTO AcceptedMissions(MissionElapse, MissionCost) VALUES (?, ?)"""
	cur.execute(sql_command, (mission.mission_time, mission.mission_cost))
	con.commit()

	return cur.lastrowid

def update_mission_details(mission_id):
	raise "update_mission_details: STUB"