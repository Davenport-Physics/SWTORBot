from game_images import init_game_images, Image
from config import *
from screenlib import ScreenImage

def main():

	init_config()
	init_game_images()
	test_screen_saving()

	return 0

def test_screen_saving():

	screen_image = ScreenImage()
	screen_image.save_image()

main()
