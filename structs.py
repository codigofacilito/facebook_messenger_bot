def typing_message(recipient_id):
	message_data = {
			'recipient': { 'id' : recipient_id },
			'sender_action': 'typing_on'
	}
	return message_data

def text_message(recipient_id, messsage_text):
	message_data = {
			'recipient': { 'id' : recipient_id },
			'message' : { 'text' : messsage_text }
	}
	return message_data


def item_quick_replie(title, payload):
	item = {
		'content_type': 'text',
		'title': title,
		'payload': payload
	}
	return item

def quick_replie_message(recipient_id, title, quick_replies):
	message_data = {
		'recipient': {'id': recipient_id},
		'message': {    
			'text': title,
			'quick_replies': quick_replies
			}
	}
	return message_data

