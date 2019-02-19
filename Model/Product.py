class Product:

	id=0


	def __init__(self, name, classement=0, score=0):
		Product.id += 1
		self.name = name
		self.features = None
		self.score = score
		self.classement = classement

	def __str__(self):
		return self.name