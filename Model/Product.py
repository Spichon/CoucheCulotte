class Product:

	id=0


	def __init__(self, name, score):
		Product.id += 1
		self.name = name
		self.features = None
		self.score = score

	def __str__(self):
		return self.name