from logic import PAGE_ID, API_KEY
import requests


def getPageAccessToken():
    url = f"https://2c1fsxykqc.execute-api.ap-southeast-1.amazonaws.com/chat-bot-mapping/get-page-token-by-page-id"
    params = {'pageId': PAGE_ID}
    headers = {'api-key': API_KEY}
    response = requests.get(url, params=params, headers=headers)
    print("response", response.json())
    return response.json()['data']["pageAccessToken"]
