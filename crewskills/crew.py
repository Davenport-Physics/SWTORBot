
from config import get_config
from screenlib import ScreenImage
from game_images import get_crew_images, get_misc_image

def need_to_scroll():

	top_scrollbar = get_misc_image("top_scrollbar.JPG")
	


def get_available_crew():

	screen_image = ScreenImage()

	crew = []
	for img in get_crew_images():
		coords = screen_image.get_coords_of_sub_image(img.opencv_image)
		if coords is not None:
			crew.append(Crew(img.name.replace(".JPG", "")))

	return crew

class Crew:

	def __init__(self, name):

		self.is_on_mission = False
		self.name = name

