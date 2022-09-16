import pyautogui
from screenlib import ScreenImage
from game_images import get_misc_image, get_crew_images
from config import get_ocr_corrected_text
import time

def get_next_available_mission():

	screen_image = ScreenImage()
	cost_image   = get_misc_image("cost")
	coords = screen_image.get_coords_of_sub_image(cost_image.opencv_image)

	if coords is None:
		raise Exception("No available mission")

	p0 = (coords[0]-309, coords[1]-14)
	p1 = (p0[0]+400, p0[1]+149)
	mission_image = screen_image.get_cropped_image(p0[0], p0[1], p1[0], p1[1])

	return CrewMission(mission_image, coords)

def manuever_mouse_to_companion_dropdown(coords):

	pyautogui.moveTo(coords[0], coords[1])
	time.sleep(0.1)
	pyautogui.click()
	time.sleep(0.1)
	pyautogui.moveTo(coords[0]+35, coords[1]+50)

def get_crew_member_name(x1, y1):

	screen_image = ScreenImage()
	cropped = screen_image.get_cropped_image(x1-310, y1-29, x1-200, y1)
	cropped.save_image("cropped_image.jpg")
	name = cropped.get_ocr_text("--psm 13 --oem 3")[0].replace("\n", "")
	return get_ocr_corrected_text(name)

def select_crew_member_for_mission(crew_member_index):

	screen_image = ScreenImage()
	companion_dropdown_image = get_misc_image("companion_dropdown")
	coords = screen_image.get_coords_of_sub_image(companion_dropdown_image.opencv_image)

	if coords is None:
		raise "Unable to find companion dropdown menu"

	manuever_mouse_to_companion_dropdown(coords)
	x1 = 0
	y1 = 0
	if crew_member_index < 3:
		x1 = coords[0]
		y1 = coords[1] + 70 + 65*crew_member_index
	else:
		for i in range(crew_member_index-2):
			pyautogui.scroll(-200)
			time.sleep(0.1)
		x1 = coords[0]
		y1 = coords[1] + 70 + 65*2
	
	crew_member_name = get_crew_member_name(x1, y1)
	pyautogui.moveTo(x1, y1)
	pyautogui.click()
	return crew_member_name

def select_mission(mission):

	pyautogui.moveTo(mission.mission_coords[0]+10, mission.mission_coords[1]+10)
	pyautogui.click()

def send_companion():

	screen_image = ScreenImage()
	send_companion_image = get_misc_image("send_companion")
	coords = screen_image.get_coords_of_sub_image(send_companion_image.opencv_image)

	if coords is None:
		raise "Unable to find send companion image"

	pyautogui.moveTo(coords[0]+10, coords[1]+10)
	pyautogui.click()



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
		try:
			self.mission_cost = int(text[0])
		except Exception as err:
			cost_text_image.save_image("cost_text_exception.jpg")
			raise err

	def init_time(self):

		time_text_image = self.mission_image.get_cropped_image(self.ref_coords[0]-75, self.ref_coords[1], self.ref_coords[0], self.ref_coords[1]+17)
		time_text       = time_text_image.get_ocr_text("--psm 13 --oem 3")[0].split(" ")

		self.mission_time = 0
		for text in time_text:
			text = text.replace("_", "").replace("\n", "").replace("a", "4")
			try:
				if 'm' in text:
					self.mission_time = self.mission_time + int(text.replace("m", ""))*60
				elif 's' in text:
					self.mission_time = self.mission_time + int(text.replace("s", ""))
			except:
				time_text_image.save_image("current_exception.jpg")
				raise Exception("Unable to parse {}".format(time_text))