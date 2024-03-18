from flask import Flask, request, Response
import json
import logic
from facebookApiSupporter import process_response

app = Flask(__name__)


@app.post("/handle-message")
def handle_message():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    data = request.json
    receivedMessage = data["receivedMessage"]
    input_message = json.loads(receivedMessage)['text']
    senderPsid = data["senderPsid"]

    response = logic.handle_message(senderPsid, input_message)
    process_response(senderPsid, response["type"], response["payload"])
    return Response("success", status=201, mimetype='application/json')


@app.post("/handle-post-back")
def handle_post_back():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    data = request.json
    payload = data["payload"]
    senderPsid = data["senderPsid"]

    response = logic.handle_post_back(senderPsid, payload)
    process_response(senderPsid, response["type"], response["payload"])
    return Response("success", status=201, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=8001)
