# client.py

import json
import websocket
import urllib.request
import urllib.parse
import requests
import uuid

from comfy_ui_client.util import _parse_queue, _find_prompt_in_history


class ComfyUIClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.ws = websocket.WebSocket()
        self.client_id = str(uuid.uuid4())

    def connect(self):
        self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")

    def close(self):
        self.ws.close()

    def get_embeddings(self):
        req = urllib.request.Request(f"http://{self.server_address}/embeddings")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result  # Assuming this is a list of strings as per your JS code

    def get_extensions(self):
        req = urllib.request.Request(f"http://{self.server_address}/extensions")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result

    def get_history(self, prompt_id):
        history_endpoint = f"http://{self.server_address}/history"
        if prompt_id is not None:
            history_endpoint = f'{history_endpoint}/{prompt_id}'
        response = urllib.request.urlopen(history_endpoint)
        return json.loads(response.read())

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result

    def interrupt(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        req = urllib.request.Request(f"http://{self.server_address}/interrupt", method='POST', headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))

    def edit_history(self, params):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = json.dumps(params).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/history", method='POST', headers=headers, data=data)
        with urllib.request.urlopen(req) as response:
            result = response.read()

    def clear_history(self):
        return self.edit_history({
            "clear": True
        })

    def delete_history(self, prompt_id_list):
        return self.edit_history({
            "delete": prompt_id_list
        })

    def get_system_stats(self):
        with urllib.request.urlopen(f"http://{self.server_address}/system_stats") as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result


    def view_metadata(self, folder_name, filename):
        params = {'filename': filename}
        url = f"http://{self.server_address}/view_metadata/{folder_name}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result

    def get_prompt(self):
        with urllib.request.urlopen(f"http://{self.server_address}/prompt") as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result

    def get_object_info(self, node_class=None):
        url = f"http://{self.server_address}/object_info"
        if node_class:
            url += f'/{node_class}'
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result

    def get_outputs(self, prompt, handle_status_event=None, handle_progress_event=None, handle_executed_event=None):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_images = {}
        if not self.ws.connected:
            self.connect()
        prompt_id = self.handle_message(prompt_id, prompt, handle_status_event, handle_progress_event, handle_executed_event)
        history = self.get_history(prompt_id)[prompt_id]
        for node_id, node_output in history['outputs'].items():
            if 'images' in node_output:
                images_output = {}
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    if image['type'] not in images_output:
                        images_output[image['type']] = {}
                    if image['subfolder'] not in images_output[image['type']]:
                        images_output[image['type']][image['subfolder']] = {}
                    images_output[image['type']][image['subfolder']][image['filename']] = image_data
                output_images[node_id] = images_output

        self.ws.close()
        return {"images": output_images}

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def upload_image(self, image_ref, image_path, overwrite=None):
        data = {"subfolder": image_ref.subfolder}
        if overwrite is not None:
            data['overwrite'] = str(overwrite)

        with open(image_path, 'rb') as image_file:
            files = {'image': (image_ref.filename, image_file)}
            resp = requests.post(f"http://{self.server_address}/upload/image", files=files, data=data)

        result = resp.json()
        if 'error' in result:
            raise Exception(json.dumps(result))

        return result

    def upload_mask(self, image_ref, image_path, overwrite=None):
        url = f"http://{self.server_address}/upload/mask"

        with open(image_path, 'rb') as image_file:
            files = {'image': (image_ref.filename, image_file)}
            data = {'original_ref': image_ref.to_json()}

            if overwrite is not None:
                data['overwrite'] = str(overwrite)

            response = requests.post(url, files=files, data=data)

        result = response.json()
        if 'error' in result:
            raise Exception(json.dumps(result))

        return result

    def get_queue(self):
        with urllib.request.urlopen(f"http://{self.server_address}/queue") as response:
            result = json.loads(response.read())
            if 'error' in result:
                raise Exception(json.dumps(result))
            return result

    def handle_message(self, prompt_id, prompt, handle_status_event=None, handle_progress_event=None, handle_executed_event=None):
        current_node = None
        while True:
            out = self.ws.recv()
            message = json.loads(out)
            if message["type"] == "status":
                if handle_status_event is not None:
                    handle_status_event(message)
                queue = self.get_queue()
                queue = _parse_queue(queue)
                if prompt_id not in queue:  # Prompt is not queued. Maybe cached
                    # Prompt is cached, so not queued. Have to fetch output info from history.
                    history = self.get_history(None)
                    cached_id = _find_prompt_in_history(history, prompt)
                    if cached_id is None:
                        raise ValueError("Cache ID not found in history")
                    return cached_id
            if message["type"] == "executing":
                if message["data"]["node"] is not None:
                    node_id = int(message["data"]["node"])
                    current_node = node_id
                    if handle_progress_event is not None:
                        handle_progress_event(current_node, 0, 0)
            if message["type"] == "executed":
                if message["data"]["prompt_id"] == prompt_id:
                    if handle_executed_event is not None:
                        handle_executed_event(message["data"])
                    break
            if message["type"] == "progress":
                progress = int(message["data"]["value"])
                total = int(message["data"]["max"])
                if handle_progress_event is not None:
                    handle_progress_event(current_node, progress, total)
        return prompt_id

# Usage example:
# client = ComfyUIClient('127.0.0.1:8188')
# client.connect()
# modified_prompt = {...}  # Your modified prompt dictionary
# output = client.get_output(modified_prompt)
# print(output)
