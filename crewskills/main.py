
import pyautogui
import time
from game_images import init_game_images, get_skill_images, get_crew_images, get_misc_image, Image
from config import *
from screenlib import ScreenImage
from crewskills import get_available_crew_skills
from crew import get_available_crew
from character import get_character_level
from grades import select_grade
from crew_mission import get_next_available_mission, select_crew_member_for_mission
from storage import *

def main():

	init_config()
	init_game_images()
	init_database()
	test_functions()

	return 0

def test_functions():

	test_screen_saving()
	test_screen_sub_image_coords()
	test_available_crew_skills()
	test_available_crew_members()
	get_character_level()
	test_grade_selection()
	test_crew_mission()

def test_available_crew_members():

	for crew in get_available_crew():
		print(crew)

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
	select_crew_member_for_mission("")


main()
