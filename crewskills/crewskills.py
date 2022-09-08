import pyautogui
from game_images import get_misc_image, get_skill_images
from screenlib import ScreenImage
from config import get_config

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
			available_skills.append(CrewSkill(img.name.replace(".JPG", ""), coords))

	return available_skills

class CrewSkill:

	def __init__(self, name, coords):

		self.name   = name
		self.coords = coords
		self.set_config()

	def __str__(self):

		return "CrewSkill(name = {}, coords = {})".format(self.name, self.coords)

	def set_config(self):

		temp = get_config()
		for crew_skill in temp["crew_skills"]:
			if crew_skill["crew_skill_name"] == self.name:
				self.config = crew_skill
				return

		raise "Unable to find appropriate config for {} crew_skill".format(self.name)

