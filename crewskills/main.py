from game_images import load_game_images
from screenlib import ScreenImage
from config import *

def main():

	init_config()
	test_screen_saving()

	return 0

def test_screen_saving():

	screen_image = ScreenImage()
	screen_image.save_image()



main()
