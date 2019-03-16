#GROUPE M2 ID APP : JAMMES PICHON PERRIN LEJEUNE
class Product:

	id=0

	def __init__(self, name, categorie=0, score=0, classement=0, features=None):
		Product.id += 1
		self.name = name
		self.features = features
		self.score = score
		self.categorie = categorie
		self.classement = classement

	def __str__(self):
		return self.name