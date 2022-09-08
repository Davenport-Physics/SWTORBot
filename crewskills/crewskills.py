import pyautogui
from game_images import get_misc_image, get_skill_images
from screenlib import ScreenImage

def crew_skills_panel_opened():

	screen_image      = ScreenImage()
	crew_skills_image = get_misc_image("crewskills.JPG")
	coords = screen_image.get_coords_of_sub_image(crew_skills_image.opencv_image)

	return coords is not None

def open_crew_skills_panel():
	
	if not crew_skills_panel_opened():
		pyautogui.press('b')

def get_available_crew_skills():

	pyautogui.moveTo(10, 10)
	pyautogui.doubleClick()
	open_crew_skills_panel()

	screen_image = ScreenImage()
	available_skills = []
	for img in get_skill_images():
		coords = screen_image.get_coords_of_sub_image(img.opencv_image)
		if coords is not None:
			available_skills.append(img.name.replace(".JPG", ""))

	return available_skills

class CrewSkill:

	def __init__(self):
		return 0

	def set_available_crew_skills(self):
		return 0