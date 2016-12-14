from flask import Flask
from flask import request

import json
from config import DevelopmentConfig

from handler import recived_message
from handler import recived_postback

from api import call_set_started_button
from api import greeting_text


app = Flask(__name__)
app.config.from_object( DevelopmentConfig )

@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
	if request.method == 'GET':
		verify_token = request.args.get('hub.verify_token', '')
		if verify_token == app.config['SECRET_KEY']:
			return request.args.get('hub.challenge', '')
		return 'Error al validar el secreto'

	elif request.method == 'POST':
		payload  = request.get_data()
		data = json.loads(payload)

		for page_entry in data['entry']:
			for message_event in page_entry['messaging']:
				#Solo mensaje
				if 'message' in message_event:
					recived_message( message_event , app.config['PAGE_ACCESS_TOKEN'], app.config['USER_GEONAMES'] )
				
				if 'postback' in message_event:
					recived_postback( message_event, app.config['PAGE_ACCESS_TOKEN'])

		return "ok"

@app.route('/', methods = ['GET'])
def index():
	return 'Hola al curso de Bot!'

if __name__ == '__main__':
	call_set_started_button( app.config['PAGE_ACCESS_TOKEN'] )
	greeting_text( app.config['PAGE_ACCESS_TOKEN'] ) 
	app.run(port = 8000)


