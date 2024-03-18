import requests
from xClassService import getPageAccessToken


def call_send_api(senderPsid, response):
    url = "https://graph.facebook.com/v16.0/me/messages"
    params = {'access_token': getPageAccessToken()}
    print("param", params)
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': senderPsid},
        'message': response
    }
    response = requests.post(url, params=params, headers=headers,
                             json=data)
    print("response", response.json())
    return response


def message(text):
    return {
        'text': text
    }


def post_back(postBackObject):
    postBack = {
        attachment: {
            type: "template",
            payload: {
                template_type: "generic",
                elements: [
                    {
                        title: postBackObject["title"],
                        subtitle: postBackObject["subtitle"],
                        buttons: map(lambda x: {
                            type: "postback",
                            title: x.title,
                            payload: x.payload
                        }, postBackObject.buttons)
                    }
                ]
            }
        }
    }
    return postBack


def quick_reply(quickReplyObject):
    quickReply = {
        text: quickReplyObject.text,
        quick_replies: map(lambda x: {
            title: x.title,
            payload: x.payload,
            content_type: text
        }, quickReplyObject.quick_replies)
    }
    return quick_reply

def process_response(senderPsid, responseType, payload):
    if responseType == "message":
        return call_send_api(senderPsid, message(payload))
    elif responseType == "post_back":
        return call_send_api(senderPsid, post_back(payload))
    elif responseType == "quick_reply":
        return call_send_api(senderPsid, quick_reply(payload))
    else:
        return "Unknown response type"
