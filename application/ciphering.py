from coding.factory import CoderFactory, Coder
from manage.factory import BufferFactory, FileManagerFactory, FileManager
from .menu import MenuEnum
from.messages import Messages

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
            MenuEnum.ENCRYPT: "Type text and encrypt.",
            MenuEnum.SAVE: "Save to file.",
            MenuEnum.DECRYPT: "Decrypt.",
            MenuEnum.PEEK: "Peek the buffer.",
            }
        self.interrupt_option = len(self.menu) + 1

        self.tasks = {
            MenuEnum.ENCRYPT: self.__task_encrypt,
            MenuEnum.SAVE: self.__task_save_to_file,
            MenuEnum.DECRYPT: self.__task_decrypt,
            MenuEnum.PEEK: self.__task_peek_the_buffer,
            self.interrupt_option: self.__task_exit
        }

    def start(self):
        self.buffer_creator = self.buffer_factory.get_buffer(self.buffer_name)

        self.file_manager = self.__get_file_manager(self.file_manager_name)
        self.buffer = None

        self.is_running = True

        print(Messages.WELCOME)
        while self.is_running:
            print(Messages.REQUEST_FOR_TASK.format(interrupt_option=self.interrupt_option))
            self.__print_menu()
            choice = self.__get_user_choice()

            task = self.tasks.get(choice, self.__unavailable)
            task()

    def __task_encrypt(self) -> tuple[str, str] | None:
        coder_name = None
        return_option = len(self.coders) + 1

        while coder_name is None:
            print(Messages.REQUEST_FOR_CODER)
            self.__print_coders()
            print(Messages.RETURN_FROM_CODERS_OPTION.format(return_option=return_option))

            choice_of_coder = self.__get_user_choice()

            if choice_of_coder == return_option:
                return

            coder_name = self.__get_coder_name(choice_of_coder)

        coder = self.__get_coder(coder_name)

        print(Messages.REQUEST_FOR_TEXT_TO_ENCODE)
        to_encode = input()

        encoded_txt = coder.encode(to_encode)

        self.buffer = self.buffer_creator(coder_name, encoded_txt)

        print(Messages.DONE)

    def __task_save_to_file(self):
        if not self.buffer:
            print(Messages.NO_BUFFER)
            return

        print(Messages.REQUEST_FOR_FILE_NAME)
        file_name = input()

        self.file_manager.save(file_name, self.buffer.data)

        self.buffer = None

        print(Messages.DONE)

    def __task_decrypt(self):
        path = self.file_manager.dir_with_saved_files
        files = os.listdir(path)

        if files:
            print(Messages.LIST_OF_FILES_PROMPT)
            self.__print_list_of_files(files)
        else:
            print(Messages.NO_FILES_PROMPT)
            return

        file_name = input()

        if file_name in files:
            data = self.file_manager.read(file_name)
            coder = self.__get_coder(data["coder"])
            decoded_text = coder.decode(data["text"])
            print(decoded_text)

        else:
            print(Messages.INVALID_FILE_NAME_PROMPT)
            return

    def __task_peek_the_buffer(self):
        if self.buffer:
            print(self.buffer.text)
        else:
            print(Messages.NO_BUFFER)

    def __task_exit(self):
        print(Messages.GOODBYE)
        self.is_running = False

    def __unavailable(self):
        return

    def __get_user_choice(self) -> int | str:
        choice = input()
        try :
            return int(choice)
        except ValueError:
            return choice

    def __print_menu(self):
        for number, action in self.menu.items():
            print(f"{number}. {action}")
        print(Messages.EXIT_TASK.format(interrupt_option=self.interrupt_option))

    def __print_coders(self):
        for number, coder in self.coders.items():
            print(f"{number}. {coder.upper()}")

    def __print_list_of_files(self, files):
        for number, file in enumerate(files, start=1):
            print(f"{number}. {file}")

    def __get_coder_name(self, coder_number: int) -> str:
        return self.coders.get(coder_number)

    def __get_coder(self, coder_name: str) -> Coder:
        return self.coder_factory.get_coder(coder_name)()

    def __get_file_manager(self, file_manager_name: str) -> FileManager:
        return self.file_manager_factory.get_file_manager(file_manager_name)()
