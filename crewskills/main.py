from game_images import init_game_images, get_skill_images, get_crew_images, Image
from config import *
from screenlib import ScreenImage
from crewskills import get_available_crew_skills

def main():

	init_config()
	init_game_images()
	test_functions()

	return 0

def test_functions():

	test_screen_saving()
	test_screen_sub_image_coords()
	test_available_crew_skills()

def test_available_crew_skills():

	for crew_skill in get_available_crew_skills():
		print(crew_skill)

def test_screen_saving():

	screen_image = ScreenImage()
	screen_image.save_image()

def test_screen_sub_image_coords():

	screen_image = ScreenImage()
	for img in get_skill_images():
		print(img.name)
		coords = screen_image.get_coords_of_sub_image(img.opencv_image)
		if coords is not None:
			screen_image.draw_circle_at_coords(coords)

	screen_image.save_image("crude_circle.jpg")


main()
