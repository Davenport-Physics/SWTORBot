
import os
import cv2  

crew_images  = []
skill_images = []
misc_images  = []

def init_game_images():

	global crew_images
	global skill_images

	crew_images  = load_images("images/crew/")
	skill_images = load_images("images/skills/")
	misc_images  = load_images("images/misc/")

def get_skill_images():

	global skill_images
	return skill_images

def get_crew_images():
	
	global crew_images
	return crew_images

def get_misc_images():

	global misc_images
	return misc_images

def get_misc_image(image_name):

	for img in misc_images:
		if img.name == image_name:
			return img

	raise "Unable to find image {}".format(image_name)


def load_images(path):

	temp = []
	for filename in os.listdir(path):
		opencv_image = cv2.imread(os.path.join(path, filename))
		temp.append(Image(filename, opencv_image))

	return temp

class Image():

	def __init__(self, name, opencv_image):
		self.name         = name
		self.opencv_image = opencv_image
