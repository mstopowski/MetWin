import json
from http.client import HTTPResponse


class JSON:
    
    @classmethod
    def save_file(cls, filelocation: str, filename: str, data: HTTPResponse):
        file = filelocation + filename
        with open(file, 'w') as json_file:
            json.dump(json.load(data), json_file)

    @classmethod
    def read_file(cls, path: str):
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        return data

    @classmethod
    def load_data_to_dict(cls, data):
        data_dict = json.loads(data.decode('utf-8'))
        return data_dict