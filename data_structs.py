from structs import typing_message
from structs import text_message
from structs import item_quick_replie
from structs import quick_replie_message
from structs import quick_replies_location
from structs import template_message_generic
from structs import element_template_message
from structs import button_item_template_message_url
from structs import button_item_template_message_postback

from structs import image_message
from structs import video_message

def create_text_message(user, data, data_model = {} ):
	messsage = data['content']
	if 'format' in data:
		messsage = messsage.format(**data_model) if 'data_model' in data else messsage.format(**user)
	return text_message(user['user_id'], messsage )

def create_quick_replies(user, data):
	replies = [ item_quick_replie(replie['title'], replie['payload']) for replie in data['replies']  ]
	data = quick_replie_message( user['user_id'], data['content'], replies )
	return data

def create_quick_replies_location(user, data):
	return quick_replies_location(user['user_id'], data['content'])

def create_typing_message(user):
	return typing_message(user['user_id'])

def create_template_message(user, data):
	elements = [  create_element_template_message(element)  for element in data['elements'] ]
	return template_message_generic(user['user_id'], elements)	

def create_element_template_message(data):
	buttons = [ create_button_item_template_message(button)  for button in data['buttons']]
	return element_template_message(data['title'], data['subtitle'], data['item_url'], data['image_url'], buttons)

def create_button_item_template_message(data):
	if data['type'] == 'web_url':
		return button_item_template_message_url(data['title'], data['url'])
	else:
		return button_item_template_message_postback(data['title'], data['payload'])

def create_image_message(user, data):
	url = data.get('url', '')
	return image_message(user['user_id'], url)

def create_video_message(user, data):
	url = data.get('url', '')
	return video_message(user['user_id'], url)


