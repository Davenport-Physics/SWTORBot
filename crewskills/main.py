from PIL import ImageGrab
from game_images import load_game_images



def main():

	load_game_images()
	img = get_screen()
	save_screen(img)

	return 0


def save_screen(img, location="test.jpg"):

	fp = open(location, "w+")
	img.save(fp)
	fp.close()

def get_screen():

	return ImageGrab.grab()

main()
