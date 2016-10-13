#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import UserModel
from models import MessageModel
import requests
import json
import datetime

from data_structs import create_text_message
from data_structs import create_quick_replies
from data_structs import create_quick_replies_location
from data_structs import create_typing_message

global_token = ''
global_username = ''

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
	validate_quick_replies(user, message)

	if user is not None:
		pass

	else:
		first_step(sender_id)

def validate_quick_replies(user, message):
	quick_reply = message.get('quick_reply', {})
	attachments = message.get('attachments', [] )

	if quick_reply or attachments:
		if quick_reply:
			set_user_reply(user, quick_reply)
		elif attachments:
			set_user_attachments(user, attachments)

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
	data = call_user_API(sender_id)
	user = UserModel.new(first_name = data['first_name'], last_name = data['last_name'], gender = data['gender'], user_id = sender_id )
	send_loop_messages(user, 'common', 'welcome' )

def send_loop_messages(user, type_message = '', context = '', data_model = {} ):
	messages = MessageModel.find_by_order(type = type_message, context = context )
	for message in messages:

		send_messages(user, message, data_model)
	
def send_messages(user, message, data_model ):
	message = get_message_data(user, message, data_model)
	typing = create_typing_message(user)

	call_send_API(typing)
	call_send_API(message)


def get_message_data(user, message, data_model = {} ):
	type_message = message['type_message']

	if type_message == 'text_message':
		return create_text_message(user, message, data_model)

	elif type_message == 'quick_replies':
		return create_quick_replies(user, message)

	elif type_message == 'quick_replies_location':
		return create_quick_replies_location(user, message)
	
def add_user_location(user, lat, lng):
	data_model = call_geoname_API(lat, lng)

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

def call_geoname_API(lat, lng):
	res = requests.get('http://api.geonames.org/findNearByWeatherJSON',
					params = {'lat': lat, 'lng': lng, 'username': global_username } )

	if res.status_code == 200:
		res = json.loads(res.text)

		city = res['weatherObservation']['stationName']
		temperature = res['weatherObservation']['temperature']
		return {'city': city, 'temperature': temperature}
		

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




