from PIL import ImageGrab
import cv2  
import numpy as np
import pytesseract

def convert_pil_image_to_cv2(image):

	return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

class ScreenImage:

	def __init__(self, image=None):

		if image is None:
			self.image = ImageGrab.grab()
		else:
			self.image = image

		self.opencv_image = convert_pil_image_to_cv2(self.image)

	def save_image(self, location="test.jpg"):

		cv2.imwrite(location, self.opencv_image)

	def save_raw_image(self, location="test.jpg"):

		with open(location, "w+") as fp :
			self.image.save(fp)

	def get_coords_of_sub_image(self, sub_image):

		result = cv2.matchTemplate(sub_image, self.opencv_image, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

		if max_val < 0.85:
			return None

		coords = np.unravel_index(result.argmax(), result.shape)

		return (coords[1], coords[0])

	def draw_circle_at_coords(self, coords):

		cv2.circle(self.opencv_image, coords, 10, (255,0,0), 2)

	def get_cropped_image(self, left, top, right, bottom):

		return ScreenImage(self.image.crop((left, top, right, bottom)))

	def get_ocr_text(self):

		gray_image = cv2.cvtColor(self.opencv_image, cv2.COLOR_BGR2GRAY)
		ret, thresh1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
		rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
		dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
		contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)

		text = []

		for cnt in contours:
			x, y, w, h = cv2.boundingRect(cnt)
			rect = cv2.rectangle(gray_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cropped = gray_image[y:y + h, x:x + w]
			text.append(pytesseract.image_to_string(cropped, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'))

		cv2.imwrite("gray_ocr_image.jpg", gray_image)


		return text