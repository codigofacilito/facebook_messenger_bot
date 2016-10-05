import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEYs') or 'SECRET_KEY'
	PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN') or 'EAARKaA1vRJsBAGEGhO2Jju41WHGEOSJi9TanA7TZBx9oLAQlukOWI6egeSZBMsPx9KiKvZBTVQZBUXgpKjWS57Jw8mMdZCv9C54yu1GugkiNh8cEQJTSM5d8tE8saBX5AKkgXFjSGWd2iySgZBlggkNPE6bSujj7bffaQpv3zrrNHv8asnjrZBO'

class DevelopmentConfig(Config):
	DEBUG = True