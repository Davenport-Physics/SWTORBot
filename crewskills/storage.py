
import sqlite3

def init_database():

	con = sqlite3.connect("crewskills.db")
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS AcceptedMission()")