import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
	PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN') or 'PAGE_ACCESS_TOKEN'

class DevelopmentConfig(Config):
	DEBUG = True