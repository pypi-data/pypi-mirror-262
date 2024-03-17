# client.py

import json
import websocket
import urllib.request
import urllib.parse
import requests
import uuid

class ComfyUIClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.ws = None 
        self.client_id = str(uuid.uuid4())

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{self.server_address}/ws?clientId={str(uuid.uuid4())}")

    def close(self):
        if self.ws:
            self.ws.close()

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        response = urllib.request.urlopen(req)
        return json.loads(response.read())

    def get_history(self, prompt_id):
        response = urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}")
        return json.loads(response.read())

    def get_outputs(self, prompt):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_images = {}
        if not self.ws:
            raise Exception("WebSocket is not connected.")
        while True:
            out = self.ws.recv()
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for node_id, node_output in history['outputs'].items():
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output

        return {"images": output_images}

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        response = urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}")
        return response.read()

    def upload_image(self, subfolder, the_file_name_on_server, image_path):
        data = {"subfolder": subfolder}
        with open(image_path, 'rb') as image_file:
            files = {'image': (the_file_name_on_server, image_file)}
            resp = requests.post(f"http://{self.server_address}/upload/image", files=files, data=data)
        return resp.content

# Usage example:
# client = ComfyUIClient('127.0.0.1:8188')
# client.connect()
# modified_prompt = {...}  # Your modified prompt dictionary
# output = client.get_output(modified_prompt)
# print(output)
