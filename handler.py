#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import UserModel
from models import MessageModel
from models import TopicModel

import datetime
import threading
import time

from api import *
from data import *

global_token = ''
global_username = ''
MAX_TIME = 2000

def recived_postback(event, token):
	sender_id = event['sender']['id']
	recipient_id = event['recipient']['id']
	time_postback = event['timestamp']
	payload = event['postback']['payload']

	global global_token
	global_token = token

	print payload

	handler_postback(sender_id, payload)

def handler_postback(user_id, payload):
	if payload == 'USER_DEFINED_PAYLOAD':
		first_step(user_id)
	else:
		user = UserModel.find(user_id = user_id)
		send_loop_messages(user, type_message='postback', context = payload)

def recived_message(event, token, username):
	sender_id = event['sender']['id']
	recipient_id = event['recipient']['id']
	time_message = event['timestamp']
	message = event['message']

	global global_token, global_username
	global_token = token
	global_username = username

	handler_action(sender_id, message)

def handler_action(sender_id, message):
	user = UserModel.find( user_id = sender_id )
	try_send_message(user, message)

def try_send_message(user, message):
	message_lower = message['text'].lower()
	message = TopicModel.get_data(message_lower)
	send_loop_messages(user, type_message=message['type'], context=message['context'])

def try_send_message_dos(user, message):
	flag = False #check_last_connection(user) or validate_quick_replies(user, message)
	
	message_lower = message['text'].lower()

	if 'ayuda' in message_lower:
		send_loop_messages(user, type_message='help', context = 'help')
	elif 'contacto desarrollador' in message_lower:
		send_loop_messages(user, type_message='develop', context='develop')
	elif 'imagen random' in message_lower:
		send_loop_messages(user, type_message='image', context='common')
	elif 'video random' in message_lower:
		send_loop_messages(user, type_message='video', context='common')
	else:
		if not flag:
			send_loop_messages(user, type_message='not_found', context='not_found')

def check_last_connection(user):
	now = datetime.datetime.now()
	last_message = user.get('last_message', now)

	user['last_message'] = now
	save_user_async(user)

	if (now - last_message).seconds >= MAX_TIME:
		programming_message(user)
		send_loop_messages(user, type_message='specific', context = 'return_user')
		return True

def validate_quick_replies(user, message):
	quick_reply = message.get('quick_reply', {})
	attachments = message.get('attachments', [] )

	if quick_reply or attachments:
		if quick_reply:
			set_user_reply(user, quick_reply)
		elif attachments:
			set_user_attachments(user, attachments)

		return True

def set_user_attachments(user, attachments):
	for attachment in attachments:
		if attachment['type'] == 'location':
			coordinates = attachment['payload']['coordinates']
			lat, lng = get_location(coordinates)

			add_user_location(user, lat, lng )
			check_actions(user, 'location')

def get_location(coordinates):
	return coordinates['lat'], coordinates['long']

def set_user_reply(user, quick_reply):
	if user is not None:
		payload = quick_reply['payload']
		preferences = user.get('preferences', [])

		if not preferences or payload not in preferences:
			preferences.append(payload)

		user['preferences'] = preferences
		UserModel.save(user)
		send_loop_messages(user, 'quick_replies', payload)

def first_step(sender_id):
	data = call_user_API(sender_id, global_token)
	user = UserModel.new(first_name = data['first_name'], last_name = data['last_name'], gender = data['gender'], user_id = sender_id, created_at = datetime.datetime.now() )
	send_loop_messages(user, 'common', 'welcome' )

def send_loop_messages(user, type_message = '', context = '', data_model = {} ):
	messages = MessageModel.find_by_order(type = type_message, context = context )
	for message in messages:
		send_messages(user, message, data_model)
	
def send_messages(user, message, data_model ):
	message = get_message_data(user, message, data_model)
	typing = create_typing_message(user)

	call_send_API(typing, global_token)
	call_send_API(message, global_token)

def get_message_data(user, message, data_model = {} ):
	type_message = message['type_message']

	if type_message == 'text_message':
		return create_text_message(user, message, data_model)

	elif type_message == 'quick_replies':
		return create_quick_replies(user, message)

	elif type_message == 'quick_replies_location':
		return create_quick_replies_location(user, message)

	elif type_message == 'template':
		return create_template_message(user, message)
	
	elif type_message == 'image':
		return create_image_message(user, message)
	
	elif type_message == 'video':
		return create_video_message(user, message)

def add_user_location(user, lat, lng):
	data_model = call_geoname_API(lat, lng, global_username)

	locations = user.get('locations', [])
	locations.append(  {'lat': lat, 'lng': lng, 'city' : data_model['city'], 'created_at' : datetime.datetime.now() } )
	user['locations'] = locations
	UserModel.save(user)

	send_loop_messages(user, 'specific', 'temperature', data_model)

def check_actions(user, action):
	actions = user.get('actions', [])

	action_structs = { action : 'Done'}
	if action_structs not in actions:
		actions.append(action_structs)
		user['actions']	= actions
		UserModel.save(user)
		
		send_loop_messages(user, type_message = 'Done', context = action)

def save_user_async(user):
	def async_method(user):
		UserModel.save(user)

	async = threading.Thread(name='async_method', target= async_method, args=(user, ))
	async.start()

def programming_message(user):
	def send_reaminer(user):
		today = datetime.datetime.today()
		future = datetime.datetime( today.year, today.month, today.day, 13, 21 )
		
		time.sleep( (future - today).seconds )
		send_loop_messages(user, type_message='remainer', context= 'remainer')

	message = threading.Thread(name='send_reaminer', target= send_reaminer, 
														args=(user, ))
	message.start()


