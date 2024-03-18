from facebookApiSupporter import call_send_api, message, post_back, quick_reply
import json


def handle_message(senderPsid, receivedMessage):
    print("receivedMessage", receivedMessage)
    input_message = json.loads(receivedMessage)['text']
    print("input_message", input_message)
    return {
        "type": "message",
        "payload": f"You have sent the message {input_message}"
    }


def handle_post_back(senderPsid, payload):
    return {
        "type": "message",
        "payload": f"You have trigger the post back type {payload}"
    }
