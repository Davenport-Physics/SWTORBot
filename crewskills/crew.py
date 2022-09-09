
from config import get_config
from screenlib import ScreenImage
from game_images import get_crew_images

def get_available_crew():

	screen_image = ScreenImage()
	for img in get_crew_images():
		coords = screen_image.get_coords_of_sub_image(img.opencv_image)
		if coords is not None:
			

