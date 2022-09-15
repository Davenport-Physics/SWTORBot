
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

	global con
	global cur

	sql_command = """INSERT INTO AcceptedMissions(MissionElapse, MissionCost) VALUES (?, ?)"""
	cur.execute(sql_command, (mission.mission_time, mission.mission_cost))
	con.commit()

	return cur.lastrowid

def update_mission_details(mission_id):

	global con
	global cur
	
	sql_command = "UPDATE AcceptedMissions SET Successful = 1 WHERE AcceptedMissionId = ?"
	cur.execute(sql_command, (mission_id))
	con.commit()

def insert_item_name_if_needed(item_name):

	global con
	global cur

	sql_command = "SELECT ItemId FROM Items WHERE ItemName = ?"
	temp = con.execute(sql_command, (item_name)).fetchone()
	if temp is not None:
		return temp[0]

	sql_command = "INSERT INTO Items(ItemName) VALUES (?)"
	cur.execute(sql_command, (item_name))
	con.commit()
		
	return cur.lastrowid


def save_retrieved_items(mission_id, item_name, amount):

	item_id = insert_item_name_if_needed(item_name)

	global con
	global cur

	sql_command = "INSERT INTO RetrievedItems(AcceptedMissionId, ItemId, Amount) VALUES (?, ?, ?)"
	cur.execute(sql_command, mission_id, item_id, amount)
	con.commit()