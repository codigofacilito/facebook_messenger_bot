from structs import text_message
from structs import item_quick_replie
from structs import quick_replie_message


def create_text_message(user, data):
	return text_message(user['user_id'], data['content'])

def create_quick_replies(user, data):
	replies = [ item_quick_replie(replie['title'], replie['payload']) for replie in data['replies']  ]
	data = quick_replie_message( user['user_id'], data['content'], replies )
	print data
	return data
