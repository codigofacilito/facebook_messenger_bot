import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEYs')
	PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
	USER_GEONAMES = os.environ.get('USER_GEONAMES')

class DevelopmentConfig(Config):
	DEBUG = True