import requests
import json

class FileReader:
    def __init__(self) -> None:
        self.info = None

    def read_document_local(self, direction):
        with open(direction, "r") as file:
            self.info = json.load(file)

    def read_document_online(self, direction):
        file = requests.get(direction)
        self.info = file.json()

    def upload_document(self, direction):
        with open(direction, "w") as file:
            json.dump(self.info, file)

    def set_info(self, info):
        self.info = info
    
    def get_info(self):
        return self.info
    
