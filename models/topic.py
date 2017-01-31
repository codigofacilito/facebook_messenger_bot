from model import Model

class Topic(Model):
	def __init__(self, database, collection_name):
		super(Topic, self).__init__(database, collection_name)

	def get_data(self, message):
		response = self.find(content=message)
		if response:
			return response['message']
		else:
			return self.get_data("default")