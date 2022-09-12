
import pyautogui
from screenlib import ScreenImage
from game_images import get_misc_image

def select_grade(grade):

	screen_image = ScreenImage()
	grade_image  = get_misc_image("grade")

	coords = screen_image.get_coords_of_sub_image(grade_image.opencv_image)
	if coords is None:
		raise "Grade Image not found"

	pyautogui.moveTo(coords[0]+10, coords[1]+10)
	pyautogui.click()
	pyautogui.moveTo(coords[0]+10, coords[1]+20 + 17*grade)
	pyautogui.click()
	pyautogui.moveTo(coords[0], coords[1])

