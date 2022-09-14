
from screenlib import ScreenImage
from game_images import get_misc_image
from config import get_config

def get_character_level():

	screen_image = ScreenImage()
	player_level_finder = get_misc_image("player_level_finder")
	coords = screen_image.get_coords_of_sub_image(player_level_finder.opencv_image)

	if coords is None:
		raise "Cannot find level. Shutting down."

	level_crop = screen_image.get_cropped_image(coords[0], coords[1], coords[0]+80, coords[1]+40)
	text = level_crop.get_ocr_text()

	return int(text[0])


def get_max_runnable_missions(character_level):

	config = get_config()
	for max_concurrent_missions in config["max_concurrent_missions"]:
		if max_concurrent_missions.min_level <= character_level:
			return max_concurrent_missions.concurrent_missions

	raise "Unable to determine max mission count"