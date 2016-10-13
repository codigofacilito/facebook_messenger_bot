from structs import typing_message
from structs import text_message
from structs import item_quick_replie
from structs import quick_replie_message
from structs import quick_replies_location

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