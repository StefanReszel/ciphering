from coding.factory import CoderFactory, Coder
from manage.factory import BufferFactory, FileManagerFactory, FileManager

import os


class Ciphering:
    def __init__(self):
        self.coder_factory = CoderFactory()
        self.coders = dict(enumerate(self.coder_factory.coders.keys(), start=1))

        self.buffer_factory = BufferFactory()
        self.buffer_name = "dict"

        self.file_manager_factory = FileManagerFactory()
        self.file_manager_name = "json"

        self.menu = { 
            1: "Type text and encrypt.",
            2: "Save to file.",
            3: "Decrypt.",
            4: "Peek the buffer.",
            }

        self.tasks = {
            1: self.task_encrypt,
            2: self.task_save_to_file,
            3: self.task_decrypt,
            4: self.task_peek_the_buffer,
        }

        self.messages = {
            "welcome": "Welcome to Cyphering!",
            "request_for_task": f"Pick 1 to {str(len(self.menu))} from menu below:",
            "bad_choice": "Typed invalid value. Try again.",
            "goodbye": "Goodbye!",
            "no_buffer": "You have nothing encrypted yet.",
        }

    def start(self):
        self.buffer_creator = self.buffer_factory.get_buffer(self.buffer_name)

        self.file_manager = self.get_file_manager(self.file_manager_name)
        self.buffer = None

        interrupt_option = len(self.tasks) + 1

        print(self.messages["welcome"])
        while True:
            print(self.messages["request_for_task"])
            self.print_menu()
            choice = self.get_user_choice()

            if choice == interrupt_option:
                print(self.messages["goodbye"])
                break

            task = self.tasks.get(choice)

            if not task:
                continue

            task()

    def task_encrypt(self) -> tuple[str, str] | None:
        request_for_coder = f"Type a number to pick the coder, or return:"
        request_for_text_to_encode = "Type your sentence to encode:"

        coder_name = None
        return_option = len(self.coders)+1

        while coder_name is None:
            print(request_for_coder)
            self.print_coders()
            print(f"{return_option}. Back.")

            choice_of_coder = self.get_user_choice()

            if choice_of_coder == return_option:
                return

            coder_name = self.get_coder_name(choice_of_coder)

        coder = self.get_coder(coder_name)

        print(request_for_text_to_encode)
        to_encode = input()

        encoded_txt = coder.encode(to_encode)

        self.buffer = self.buffer_creator(coder_name, encoded_txt)

        print("Done!")

    def task_save_to_file(self):
        if not self.buffer:
            print(self.messages["no_buffer"])
            return

        request_for_file_name = "Type the file name where data will be saved:"
        
        print(request_for_file_name)
        file_name = input()

        self.file_manager.save(file_name, self.buffer.data)

        self.buffer = None

        print("Done!")

    def task_decrypt(self):
        list_of_files_prompt = "Type a full name of file from the list below:"
        no_files_prompt = "There are no files to decrypt."
        invalid_file_name_prompt = "Invalid file's name. Try again."

        path = self.file_manager.dir_with_saved_files
        files = os.listdir(path)

        if files:
            print(list_of_files_prompt)
            self.print_list_of_files(files)
        else:
            print(no_files_prompt)
            return

        file_name = input()

        if file_name in files:
            data = self.file_manager.read(file_name)
            coder = self.get_coder(data["coder"])
            decoded_text = coder.decode(data["text"])
            print(decoded_text)

        else:
            print(invalid_file_name_prompt)
            return

    def task_peek_the_buffer(self):
        if self.buffer:
            print(self.buffer.text)
        else:
            print(self.messages["no_buffer"])

    def get_user_choice(self) -> int | str:
        choice = input()
        try :
            return int(choice)
        except ValueError:
            return choice

    def print_menu(self):
        for number, action in self.menu.items():
            print(f"{number}. {action}")
        print(f"{len(self.menu)+1}. Exit.")

    def print_coders(self):
        for number, coder in self.coders.items():
            print(f"{number}. {coder.upper()}")

    def print_list_of_files(self, files):
        for number, file in enumerate(files, start=1):
            print(f"{number}. {file}")

    def get_coder_name(self, coder_number: int) -> str:
        return self.coders.get(coder_number)

    def get_coder(self, coder_name: str) -> Coder:
        return self.coder_factory.get_coder(coder_name)()

    def get_file_manager(self, file_manager_name: str) -> FileManager:
        return self.file_manager_factory.get_file_manager(file_manager_name)()
