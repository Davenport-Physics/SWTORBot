
import pyautogui
from screenlib import ScreenImage
from game_images import get_misc_image
import time

def get_quantity_of_items(x1, y1):

	screen_image = ScreenImage()
	cropped = screen_image.get_cropped_image(x1+6, y1+8, x1+28, y1+23)
	number  = cropped.get_ocr_text()[0]
	try:
		return int(number)
	except Exception as err:
		cropped.log_image("get_quantity_of_items: Unable to parse image: {}".format(number))
		cropped = screen_image.get_cropped_image(x1+6, y1+8, x1+25, y1+23)

		try:		
			number = cropped.get_ocr_text()[0]
			return int(number)
		except:
			cropped.log_image("get_quantity_of_items: Unable to parse secondary image: {}".format(number))

	return -1


def get_item_name(x1, y1):

	screen_image = ScreenImage()
	cropped = screen_image.get_cropped_image(x1-280, y1+35, x1-200, y1+70)
	return cropped.get_ocr_text("--psm 13 --oem 3")[0].replace("\n", "")

def get_description(x1, y1):

	screen_image = ScreenImage()
	cropped = screen_image.get_cropped_image(x1, y1-75, x1+100, y1-50)
	return cropped.get_ocr_text("--psm 13 --oem 3")[0].replace("\n", "")

def get_mission_complete():

	screen_image = ScreenImage()
	accept_coords = screen_image.get_coords_of_sub_image(get_misc_image("mission_accept").opencv_image)
	if accept_coords is None:
		raise Exception("Unable to find accept reference coords")

	provided_coords = screen_image.get_coords_of_sub_image(get_misc_image("provided_rewards").opencv_image)
	if provided_coords is None:
		raise Exception("Unable to find provided rewards")

	quantity_of_items = get_quantity_of_items(provided_coords[0]+20, provided_coords[1]+40)
	pyautogui.moveTo(provided_coords[0]+20, provided_coords[1]+40)
	time.sleep(0.5)
	item_name   = get_item_name(provided_coords[0]+20, provided_coords[1]+40)
	description = get_description(provided_coords[0], provided_coords[1])

	pyautogui.moveTo(accept_coords[0]+5, accept_coords[1]+5)
	pyautogui.click()
	pyautogui.moveTo(10, 10)
	time.sleep(0.1)

	return MissionComplete(description, item_name, quantity_of_items)


class MissionComplete:

	def __init__(self, description, item_name, quantity_of_items):

		self.description       = description
		self.item_name         = item_name
		self.quantity_of_items = quantity_of_items

	def __str__(self):

		return "MissionComplete(description = {}, item_name = {}, quantity_of_items = {})".format(self.description, self.item_name, self.quantity_of_items)