import pyautogui
from screenlib import ScreenImage
from game_images import get_misc_image

def get_next_available_mission():

	screen_image = ScreenImage()
	cost_image   = get_misc_image("cost")
	coords = screen_image.get_coords_of_sub_image(cost_image.opencv_image)

	if coords is None:
		raise "No available mission"

	p0 = (coords[0]-309, coords[1]-14)
	p1 = (p0[0]+400, p0[1]+149)
	mission_image = screen_image.get_cropped_image(p0[0], p0[1], p1[0], p1[1])
	mission_image.save_image("mission_image.jpg")

	return CrewMission(mission_image)

class CrewMission:

	def __init__(self, mission_image):
		
		self.mission_image = mission_image
		self.init_cost()
		self.init_time()

	def init_cost(self):

		cost_image      = get_misc_image("cost")
		coords          = self.mission_image.get_coords_of_sub_image(cost_image.opencv_image)
		cost_text_image = self.mission_image.get_cropped_image(coords[0], coords[1], coords[0]+102, coords[1]+17)
		text = cost_text_image.get_ocr_text()
		print("mission_cost = {}".format(int(text[0])))
		self.mission_cost = int(text[0])

	def init_time(self):

		cost_image = get_misc_image("cost")
		coords     = self.mission_image.get_coords_of_sub_image(cost_image.opencv_image)
		time_text_image = self.mission_image.get_cropped_image(coords[0]-102, coords[1], coords[0], coords[1]+17)
		time_text_image.save_image("time_text_image.jpg")
		print(time_text_image.get_ocr_text())