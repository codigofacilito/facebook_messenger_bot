#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import UserModel
from models import MessageModel
import requests
import json

from data_structs import create_text_message
from data_structs import create_quick_replies

global_token = ''

def recived_message(event, token):
	sender_id = event['sender']['id']
	recipient_id = event['recipient']['id']
	time_message = event['timestamp']
	message = event['message']
	text = message['text']

	global global_token
	global_token = token

	handler_action(sender_id)

def handler_action(sender_id ):
	user = UserModel.find( user_id = sender_id )
	if user is not None: #Si se encuentra en la base de datos
		message = 'Gracias por regresar'
		
		typing = typing_message(sender_id)
		call_send_API(typing)

		message = text_message(sender_id, message )
		call_send_API(message)
	else:
		first_step(sender_id)
	
def first_step(sender_id):
	data = call_user_API(sender_id)
	user = UserModel.new(first_name = data['first_name'], last_name = data['last_name'], gender = data['gender'], user_id = sender_id )
	send_loop_messages(user, 'common', 'welcome' )

def send_loop_messages(user, type_message = '', context = ''):
	messages = MessageModel.find_by_order(type = type_message, context = context )
	for message in messages:

		message = get_message_data(user, message)
		call_send_API(message)
	
def get_message_data(user, message):
	type_message = message['type_message']

	if type_message == 'text_message':
		return create_text_message(user, message)

	elif type_message == 'quick_replies':
		return create_quick_replies(user, message)

def call_send_API( data ):
	res = requests.post('https://graph.facebook.com/v2.6/me/messages',
					params = {'access_token': global_token },
					data = json.dumps(data),
					headers = { 'Content-type': 'application/json' }
					)
	if res.status_code == 200:
		print "El mensaje fue enviado exitosamente!"

def call_user_API(user_id ):
	res = requests.get('https://graph.facebook.com/v2.6/' + user_id ,
					params = {'access_token': global_token } )

	data = json.loads(res.text)
	return data




