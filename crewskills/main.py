
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
from crew_mission_complete import get_mission_complete
from storage import *
from random import uniform


def main():

	init_config()
	init_game_images()
	init_database()
	#test_storage()
	#test_crew_mission_complete()
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
		self.reset_required          = False
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
			time.sleep(3.0)
			self.loop()

	def set_first_missions(self):

		grade_selector = GradeSelector(self.player_config["grades_to_auto"])
		current_grade  = grade_selector.get_next_grade()

		for i in range(min([self.max_concurrent_missions, self.num_crew_members])):

			print(i)
			select_grade(current_grade)
			time.sleep(uniform(0.25, 1.0))
			crew_member = select_crew_member_for_mission(i)
			time.sleep(uniform(0.25, 1.0))
			try:
				mission = get_next_available_mission()
				self.current_missions.append(Assignment(mission, crew_member, i))
				select_mission(mission)
				time.sleep(uniform(0.25, 1.0))
				send_companion()
			except:
				i = i - 1
				current_grade  = grade_selector.get_next_grade()


	def loop(self):

		self.handle_reset()
		self.finish_missions()
		self.schedule_missions()

	def handle_reset(self):

		if not self.reset_required:
			return

		finished_assignments = list(filter(lambda assignment: assignment.finished_and_stored, self.current_missions))
		if len(finished_assignments) == min(self.num_crew_members, self.max_concurrent_missions):
			self.reset_required   = False
			self.current_missions = []
			self.set_first_missions()


	def finish_missions(self):

		finished_assignments = list(filter(lambda missions: missions.time_until_completion < time.time() and not missions.finished_and_stored, self.current_missions))
		finished_missions    = []

		for i in range(len(finished_assignments)):
			print(finished_assignments[i])

		while True:
			time.sleep(uniform(1.0, 2.0))
			try:
				mission_complete = get_mission_complete()
				print(mission_complete)
				finished_missions.append(mission_complete)
			except Exception as err:
				print(err)
				break

		for assignment in finished_assignments:
			relevant_missions = list(filter(lambda mission: assignment.crew_member_name in mission.description, finished_missions))
			if len(relevant_missions) > 0:
				assignment.finish(relevant_missions)


	def schedule_missions(self):

		if self.reset_required:
			return

		grade_selector = GradeSelector(self.player_config["grades_to_auto"])
		current_grade  = grade_selector.get_next_grade()
		assignments    = list(filter(lambda crew: crew.finished_and_stored, self.current_missions))
		for i in range(len(assignments)):

			select_grade(current_grade)
			time.sleep(uniform(0.25, 1.0))
			temp_crew_member_name = select_crew_member_for_mission(assignments[i].dropdown_index)

			if temp_crew_member_name != assignments[i].crew_member_name:
				print("reset_required = True. {} != {}".format(temp_crew_member_name, assignments[i].crew_member_name))
				self.reset_required = True
				break

			time.sleep(uniform(0.25, 1.0))
			try:
				mission = get_next_available_mission()
				assignments[i].set_new_mission(mission)
				select_mission(mission)
				time.sleep(uniform(0.25, 1.0))
				send_companion()
			except:
				i = i - 1
				current_grade = grade_selector.get_next_grade()




class GradeSelector:

	def __init__(self, grades):

		self.grades = grades.copy()

	def get_next_grade(self):

		current_grade = max(self.grades)
		self.grades = list(filter(lambda x: x != current_grade, self.grades))
		return current_grade



class Assignment:

	def __init__(self, mission, crew_member_name, dropdown_index):

		self.mission               = mission
		self.crew_member_name      = crew_member_name
		self.dropdown_index        = dropdown_index
		self.time_until_completion = time.time() + mission.mission_time
		self.finished_and_stored   = False
		self.mission_id = save_mission_details(mission, crew_member_name)

	def __str__(self):

		return "Assignment(missions = {}, crew_member_name = {}, mission_id = {})".format(self.mission, self.crew_member_name, self.mission_id)

	def set_new_mission(self, mission):

		self.mission               = mission
		self.time_until_completion = time.time() + mission.mission_time
		self.finished_and_stored   = False
		self.mission_id = save_mission_details(mission, self.crew_member_name)

	def finish(self, finished_missions):

		for temp in finished_missions:
			save_retrieved_items(self.mission_id, temp.item_name, temp.quantity_of_items)

		self.finished_and_stored = True



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

def test_crew_mission_complete():

	pyautogui.moveTo(10, 10)
	pyautogui.doubleClick()
	print(get_mission_complete())

def test_storage():

	print(insert_item_name_if_needed("Desh"))

main()
