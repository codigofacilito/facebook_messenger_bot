import os

class Config(object):
	SECRET_KEY = 'SECRET_KEY'
	PAGE_ACCESS_TOKEN = 'EAAD2l6mkZANkBAKfDV5AZB6N0j7qmaG7kVIwlnhnZCIJcb1tGK9zMZCOXwqxQZCJB3MZAIu5zs0hoA361c9CKNxjkiVFqZByKpaE55HDBruVlLvg8G46ZAZBJenyZAxl2qOBP0loGoZAzEZBRcQM7lzb6dktAZBeCtfuwQevG5JeP61WNF0wZAxW4tvS3m'
	USER_GEONAMES = os.environ.get('USER_GEONAMES')

class DevelopmentConfig(Config):
	DEBUG = True