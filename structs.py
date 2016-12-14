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

def quick_replies_location(recipient_id, title):
	message_data = {
		'recipient': {'id': recipient_id},
		'message': {    
			'text': title,
			'quick_replies': [
					{
						'content_type' : 'location',
					}
				]
			}
	}
	return message_data

def button_item_template_message_url(title, url):
    button = {  "type": "web_url",
                "title": title,
                "url": url }
    return button

def button_item_template_message_postback(title, payload):
    button = {  "type": "postback",
                "title": title,
                "payload": payload }
    return button
 
def element_template_message(title, subtitle, item_url, image_url, buttons):
	item = { 
	    "title": title,
	    "subtitle": subtitle,
	    "item_url": item_url,
	    "image_url": image_url,
	    "buttons": buttons
    }
	return item

def template_message_generic(recipient_id, elements):
	message_data = {
        "recipient":{ "id":recipient_id},
        "message":{
            "attachment":
                {
                    "type":"template",
                    "payload":
                    {
                        "template_type": "generic",
                        "elements": elements
                    }
                }
        }
    }
	return message_data 



def image_message(recipient_id, url):
	message_data = {
		'recipient': { 'id': recipient_id },
		'message': {
			'attachment': {
				'type': 'image',
				'payload': {
					'url': url
				}
			}
		}
	}
	return message_data


def video_message(recipient_id, url):
	message_data = {
		'recipient': { 'id': recipient_id },
		'message': {
			'attachment': {
				'type': 'video',
				'payload': {
					'url': url
				}
			}
		}
	}
	return message_data









