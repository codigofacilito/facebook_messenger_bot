class Model(object):
	def __init__(self, database, collection_name):
		self.database = database
		self.collection_name = collection_name
		self.collection = database[self.collection_name]

	def new(self, **kwargs):
		return self.save(kwargs)

	def save(self, document):
		self.collection.save(document)
		return document

	def find(self, **kwargs):
		return self.collection.find_one(kwargs)

	def find_all(self, **kwargs):
		return self.collection.find(kwargs)

	def delete_collection(self):
		self.collection.delete_many({})