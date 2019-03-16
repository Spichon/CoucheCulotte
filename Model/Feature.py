#GROUPE M2 ID APP : JAMMES PICHON PERRIN LEJEUNE
class Feature:

	id=0

	def __init__(self, name, notation, poids):
		Feature.id += 1
		self.name = name
		self.notation = notation
		self.poids = poids

	def __str__(self):
		return (self.name)

