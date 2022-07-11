import json
import requests
class APIExecutor:
    def __init__(self):
        self.url = 'http://gocibot-api.eng.vmware.com/api/v1/'
        self.headers = {'X-API-KEY': '671c2d2b-62d8-4eee-876b-f5efbf314d22',
                      'Accept': 'Application/json',
                      'Content-type': 'Application/json'}
    def do_get(self, urlpart2):
        self.url = self.url + urlpart2
        print(type(self.url))
        response = requests.get(self.url, headers=self.headers)
        response = requests.get(self.url)
        return response.json()
    def do_post(self, urlpart2, payload):
        payload = json.dumps(payload)
        self.url = self.url + urlpart2
        response = requests.post(self.url, headers=self.headers, data=payload)
        return response.json()
