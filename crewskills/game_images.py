
import os

def load_game_images():

	crew_images = load_images("images/crew/")
	skill_images = load_images("images/skills/")

	for i in range(len(crew_images)):
		print(crew_images[i].name)

def load_images(path):

	temp = []
	for filename in os.listdir(path):
		with open(os.path.join(path, filename), "rb") as f:
			data = f.read()
			temp.append(Image(filename, data))

	return temp


class Image():

	def __init__(self, name, data):
		self.name = name
		self.data = data
