import os

class Config(object):
	SECRET_KEY = 'SECRET_KEY'
	PAGE_ACCESS_TOKEN = 'EAAP8ySrcUEkBAIcAv6ARELYNiZBGXUHpArq0WmmSbCMFZCU13phbAYQK6RC3Nonk6CsrLFFrWuay4xZBHjQ2fygxl6at4dZCKLQyBR32MW119pkcGHe4EnZBhCPTfC7ol7dtGQ7OY9G7Tyabyt9HcelTanoq0mG2JxqXsM4dHhro58a9ZB6kkZC'
	USER_GEONAMES = os.environ.get('USER_GEONAMES')

class DevelopmentConfig(Config):
	DEBUG = True