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
	#mission_image.save_image("mission_image.jpg")

	return CrewMission(mission_image, coords)

class CrewMission:

	def __init__(self, mission_image, mission_coords):
		
		self.mission_image = mission_image

		cost_image          = get_misc_image("cost")
		self.ref_coords     = self.mission_image.get_coords_of_sub_image(cost_image.opencv_image)
		self.mission_coords = mission_coords

		self.init_cost()
		self.init_time()

	def init_cost(self):

		cost_text_image   = self.mission_image.get_cropped_image(self.ref_coords[0], self.ref_coords[1], self.ref_coords[0]+102, self.ref_coords[1]+17)
		text              = cost_text_image.get_ocr_text()
		self.mission_cost = int(text[0])

	def init_time(self):

		time_text_image = self.mission_image.get_cropped_image(self.ref_coords[0]-75, self.ref_coords[1], self.ref_coords[0], self.ref_coords[1]+17)
		time_text       = time_text_image.get_ocr_text("--psm 13 --oem 3")[0].split(" ")

		self.mission_time = 0
		for text in time_text:
			if 'm' in text:
				self.mission_time = self.mission_time + int(text.replace("m", ""))*60
			elif 's' in text:
				self.mission_time = self.mission_time + int(text.replace("s", ""))