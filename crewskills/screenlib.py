from PIL import ImageGrab
import cv2  
import numpy as np

def convert_pil_image_to_cv2(image):

	return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

class ScreenImage:

	def __init__(self):

		self.image = ImageGrab.grab()
		self.opencv_image = convert_pil_image_to_cv2(self.image)

	def save_image(self, location="test.jpg"):

		cv2.imwrite(location, self.opencv_image)

	def save_raw_image(self, location="test.jpg"):

		with open(location, "w+") as fp :
			self.image.save(fp)

	def get_coords_of_sub_image(self, sub_image):

		result = cv2.matchTemplate(sub_image, self.opencv_image, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

		if max_val < 0.9:
			return None

		return np.unravel_index(result.argmax(), result.shape)

	def draw_circle_at_coords(self, coords):

		cv2.circle(self.opencv_image, (coords[1], coords[0]), 10, (255,0,0), 2)