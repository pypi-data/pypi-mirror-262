import requests
import json
import time
import os

class pixaiAPI:
    payloads_path = "api/payloads.json"  

    def __init__(self, token):
        self.base_url = "https://api.pixai.art/graphql"
        self.headers = {
            'User-Agent': "Mozilla/5.0",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/json"
        }
        self.json_payload = self.load_json_payload()  

    @classmethod
    def load_json_payload(cls):
        with open(cls.payloads_path, encoding='utf-8') as f:
            return json.load(f)

    def send_request(self, payload):
        try:
            resp = requests.post(self.base_url, json=payload, headers=self.headers)
            return resp.json() if resp.ok else self._handle_error(resp)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None 
    

    def createGenerationTask(self, prompts=None, steps=None, modelId=None, samplingMethod=None, cfgScale=None, width=None, height=None):
        payload = self.json_payload['createGenerationTask']
        parameters = payload['variables']['parameters']

        parameters['prompts'] = prompts if prompts is not None else parameters['prompts']
        parameters['samplingSteps'] = steps if steps is not None else parameters['samplingSteps']
        parameters['modelId'] = modelId if modelId is not None else parameters['modelId']
        parameters['samplingMethod'] = samplingMethod if samplingMethod is not None else parameters['samplingMethod']
        parameters['cfgScale'] = cfgScale if cfgScale is not None else parameters['cfgScale']
        parameters['width'] = width if width is not None else parameters['width']
        parameters['height'] = height if height is not None else parameters['height']

        response = self.send_request(payload)
        
        if "error" in response:
            print(f"Failed to create task due to error: {response['error'].get('message')}")
        else:
            task_id = response.get('data', {}).get('createGenerationTask', {}).get('id')
            if task_id:
                print(f"Task ID: {task_id}")
            else:
                print("Failed to create task or get a response")
            return task_id

    def getTaskById(self, task_id):
        time.sleep(6)  
        self.json_payload['getTaskById']['variables']['id'] = task_id
        payload = self.json_payload['getTaskById']
        response = self.send_request(payload)
        
        # getting image url
        public_urls = [url_info['url'] for url_info in response.get('data', {}).get('task', {}).get('media', {}).get('urls', []) if url_info.get('variant') == "PUBLIC"]
        
        if public_urls: 
            return public_urls[0]

    def DownloadImage(self, url):
        filename = f"{os.path.splitext(os.path.basename(url))[0]}.png"
        rimage = requests.get(url).rimage
        with open(filename, 'wb') as file:
            file.write(rimage)
        return filename

    @staticmethod
    def _handle_error(response):
        print(f"Error: {response.status_code}, {response.text}")
        return None