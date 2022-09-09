
import pyautogui
import time
from config import get_config
from screenlib import ScreenImage
from game_images import get_crew_images, get_misc_image

def setup_mouse_scrolling(screen_image):

	top_scrollbar = get_misc_image("top_scrollbar")
	coords = screen_image.get_coords_of_sub_image(top_scrollbar.opencv_image)
	if coords is not None:
		pyautogui.moveTo(coords[0], coords[1]+20)

	return coords is not None


def available_crew_in_segment():

	crew = []
	screen_image = ScreenImage()
	for img in get_crew_images():
		coords = screen_image.get_coords_of_sub_image(img.opencv_image)
		if coords is not None:
			crew.append(Crew(img.name))

	return crew

def get_available_crew():

	screen_image = ScreenImage()

	scroll_times = 1
	if setup_mouse_scrolling(screen_image):
		scroll_times = 6

	crew = []
	for i in range(scroll_times):
		for crew_segment in available_crew_in_segment():
			if len(list(filter(lambda temp : temp.name == crew_segment.name, crew))) == 0:
				crew.append(crew_segment)
		pyautogui.scroll(-200)
		time.sleep(0.5)

	pyautogui.scroll(1200)

	return crew

class Crew:

	def __init__(self, name):

		self.is_on_mission = False
		self.name = name

	def __str__(self):

		return "Crew(name = {})".format(self.name)

