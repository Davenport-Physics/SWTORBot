from PIL import ImageGrab
import cv2  
import numpy as np

class ScreenImage:

	def __init__(self):

		self.image = ImageGrab.grab()
		self.opencv_image = convert_pil_image_to_cv2(self.image)

	def save_image(self, location="test.jpg"):

		with open(location, "w+") as fp :
			self.image.save(fp)

	def get_coords_of_sub_image(self, sub_image):

		result = cv2.matchTemplate(sub_image, self.opencv_image, cv2.TM_CCOEFF_NORMED)  
		return np.unravel_index(result.argmax(), result.shape)

def convert_pil_image_to_cv2(image):

	return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)