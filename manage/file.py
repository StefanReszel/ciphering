from .abstract import FileManager
import json


class JSONManager(FileManager):
    def save(self, file_name, content: dict):
        json_data = json.dumps(content, indent=2)
        file_name = f"{file_name}.json"
        super().save(file_name, json_data)

    def get_coder_name_and_text_from_file(self, file_content):
        file_data = json.loads(file_content)
        return file_data["coder"], file_data["text"]
