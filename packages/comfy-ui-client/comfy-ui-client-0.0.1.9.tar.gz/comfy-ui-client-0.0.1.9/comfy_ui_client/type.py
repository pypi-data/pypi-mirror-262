import json


class ImageRef:
    def __init__(self, filename, subfolder="", type=""):
        self.filename = filename
        self.subfolder = subfolder
        self.type = type

    def to_json(self):
        data = {
            'filename': self.filename,
            'subfolder': self.subfolder,
            'type': self.type
        }
        return json.dumps(data)
