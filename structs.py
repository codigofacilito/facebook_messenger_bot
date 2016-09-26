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