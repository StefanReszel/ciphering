from .abstract import FileManager
import json


class JSONManager(FileManager):
    def save(self, file_name: str, content: dict):
        json_data = json.dumps(content, indent=2)
        file_name = f"{file_name}.json"
        super().save(file_name, json_data)

    def read(self, file_name: str) -> dict:
        file_content = super().read(file_name)
        data = json.loads(file_content)
        return data
