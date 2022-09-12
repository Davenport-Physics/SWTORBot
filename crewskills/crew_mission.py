import pyautogui
from screenlib import ScreenImage
from game_images import get_misc_image

def get_next_available_mission():

	screen_image = ScreenImage()
	cost_image   = get_misc_image("cost")
	coords = screen_image.get_coords_of_sub_image(cost_image.opencv_image)

	if coords is None:
		raise "No available mission"

	p0 = (coords[0]-309, coords[1]-10)
	p1 = (p0[0]+395, p0[1]+140)
	mission_image = screen_image.get_cropped_image(p0[0], p0[1], p1[0], p1[1])

	return CrewMission(mission_image, coords)

class CrewMission:

	def __init__(self, mission_image, ref_coords):
		
		self.mission_image = mission_image
		self.ref_coords    = ref_coords

		