
import pyautogui
import time
from game_images import init_game_images, get_skill_images, get_crew_images, get_misc_image, Image
from config import *
from screenlib import ScreenImage
from crewskills import get_available_crew_skills
from crew import get_available_crew
from character import get_character_level, get_max_runnable_missions
from grades import select_grade
from crew_mission import get_next_available_mission, select_crew_member_for_mission, select_mission, send_companion
from storage import *


def main():

	init_config()
	init_game_images()
	init_database()
	#test_functions()

	crew_skill_runner = CrewSkillRunner()
	crew_skill_runner.start()
	return 0


class CrewSkillRunner:

	def __init__(self):

		self.crew_skills             = get_available_crew_skills()
		self.num_crew_members        = len(get_available_crew())
		self.character_level         = get_character_level()
		self.max_concurrent_missions = get_max_runnable_missions(self.character_level)
		self.ongoing_missions_count  = 0
		self.player_config           = get_player_config()
		self.current_missions        = []
		self.open_mission_window()

	def open_mission_window(self):

		for crew_skill in self.crew_skills:
			if crew_skill.name == self.player_config["crew_skill_to_auto"]:
				pyautogui.moveTo(crew_skill.coords[0] + 2, crew_skill.coords[1] + 2)
				pyautogui.click()
				break

	def start(self):

		self.set_first_missions()

		while True:
			time.sleep(1.0)
			#self.loop()

	def set_first_missions(self):

		available_grades = self.player_config["grades_to_auto"].copy()
		current_grade    = max(available_grades)
		available_grades = filter(lambda x: x != current_grade, available_grades)

		for i in range(min([self.max_concurrent_missions, self.num_crew_members])):

			select_grade(current_grade)
			time.sleep(0.5)
			crew_member = select_crew_member_for_mission(i)
			time.sleep(0.25)
			try:
				mission = get_next_available_mission()
				self.current_missions.append(Assignment(mission, crew_member))
				select_mission(mission)
				send_companion()
			except:
				i = i - 1
				current_grade    = max(available_grades)
				available_grades = available_grades.where(lambda x: x != current_grade)


	def loop(self):

		self.finish_missions()
		self.schedule_missions()

	def finish_missions(self):

		for i in range(len(current_missions)):
			raise "Nothing"

		raise "Nothing"

	def schedule_missions(self):

		if self.ongoing_missions_count == self.num_crew_members:
			return

		mission_diff = self.max_concurrent_missions - self.ongoing_missions_count
		for i in range(mission_diff):
			raise "None"

class Assignment:

	def __init__(self, mission, crew_member):
		self.mission               = mission
		self.crew_member           = crew_member
		self.time_until_completion = time.time() + mission.mission_time

	


def test_functions():

	test_screen_saving()
	test_screen_sub_image_coords()
	test_available_crew_skills()
	crew_members = test_available_crew_members()
	get_character_level()
	test_grade_selection()
	test_crew_mission()

def test_available_crew_members():

	crew_members = get_available_crew()
	for crew in crew_members:
		print(crew)

	return crew_members

def test_available_crew_skills():

	crew_skills = get_available_crew_skills()
	for crew_skill in crew_skills:
		print(crew_skill)
		pyautogui.moveTo(crew_skill.coords[0] + 2, crew_skill.coords[1] + 2)
		pyautogui.click()
		time.sleep(0.1)

	#pyautogui.press('esc')
	#pyautogui.press('esc')


def test_screen_saving():

	screen_image = ScreenImage()
	screen_image.save_image()

def test_screen_sub_image_coords():

	screen_image = ScreenImage()
	for img in get_skill_images():
		print("testing_sub_image_coords {}".format(img.name))
		coords = screen_image.get_coords_of_sub_image(img.opencv_image)
		if coords is not None:
			screen_image.draw_circle_at_coords(coords)

def test_grade_selection():

	select_grade(5)

def test_crew_mission():

	mission = get_next_available_mission()
	save_mission_details(mission)
	print("Mission information: time(s) -> {} cost: -> {}".format(mission.mission_time, mission.mission_cost))
	select_crew_member_for_mission(0)
	#select_mission(mission)
	#send_companion()


main()
