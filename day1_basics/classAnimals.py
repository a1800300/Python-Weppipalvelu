class Animal():
	name = "Generic animal"

	def sound(self):
		return   "Generic cute animal sounds"

class Lion(Animal):
	def sound(self):
	return "Roaaaaar!"


def main():
	lion = Lion()
	print(lion.sound())
