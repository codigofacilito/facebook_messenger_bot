from model import Model

class User(Model):
	def __init__(self, database, collection_name):
		super(User, self).__init__(database, collection_name)