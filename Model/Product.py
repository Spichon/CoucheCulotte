class Product:

	id=0


	def __init__(self, name, score):
		Product.id += 1
		self.name = name
		self.features = []
		self.score = score

	def __str__(self):
		return self.name


	def add_feature(self, feature):
		self.features.append(feature)

	def remove_feature(self, feature):
		self.features.remove(feature)