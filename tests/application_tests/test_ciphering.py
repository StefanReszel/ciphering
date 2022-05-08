from unittest.mock import Mock, PropertyMock, call
from application.ciphering import Ciphering, Coder, FileManager
from application.menu import MenuEnum
import pytest


class TestCiphering:
    @pytest.fixture
    def app(self):
        return Ciphering()

    @pytest.fixture
    def file_data(self, app):
        return {"coder": app.coders[1], "text": "test_text"}

    @pytest.fixture
    def file_manager_mock(self, app, file_data):
        file_manager = app.file_manager = Mock(name="file_manager")
        file_manager.read.return_value = file_data
        return file_manager

    @pytest.fixture
    def input_mock(self, mocker):
        value = "test"
        mocker.patch("application.ciphering.input", return_value=value)
        return value

    @pytest.fixture
    def os_listdir_mock(self, mocker):
        mocker.patch("application.ciphering.os.listdir", return_value=["test"])

    @pytest.fixture
    def coder_getter_mock(self, mocker):
        return mocker.patch("application.ciphering.Ciphering._Ciphering__get_coder")

    @pytest.fixture
    def coder_mock(self, coder_getter_mock):
        return coder_getter_mock()

    @pytest.fixture
    def get_coder_name_mock(self, mocker):
        return mocker.patch("application.ciphering.Ciphering._Ciphering__get_coder_name")

    @pytest.fixture
    def buffer_creator_mock(self, app):
        buffer_creator = app.buffer_creator = Mock(name="app.buffer_creator")
        return buffer_creator

    @pytest.fixture
    def user_choice(self, mocker, request):
        mocker.patch("application.ciphering.Ciphering._Ciphering__get_user_choice", return_value=request.param)

    @pytest.fixture
    def set_buffer_attribute(self, app):
        app.buffer = Mock(name="app.buffer")

    @pytest.fixture
    def while_loop_iteration_control(self, app, request):
        type(app).is_running = PropertyMock(side_effect=[True, True, False])

        def del_attr():
            del type(app).is_running
        request.addfinalizer(del_attr)


    @pytest.mark.parametrize("user_choice", [MenuEnum.ENCRYPT], indirect=True)
    def test_start_should_invoke_task_encrypt_from_tasks_dict_when_user_chose_menu_enum_encrypt(self,
        while_loop_iteration_control, app, user_choice):
        task_encrypt_mock = app.tasks[MenuEnum.ENCRYPT] = Mock(name="task_encrypt")
        
        app.start()

        assert task_encrypt_mock.called


    @pytest.mark.parametrize("user_choice", [MenuEnum.SAVE], indirect=True)
    def test_start_should_invoke_task_encrypt_from_tasks_dict_when_user_chose_menu_enum_save(self,
        while_loop_iteration_control, app, user_choice):
        task_save_mock = app.tasks[MenuEnum.SAVE] = Mock(name="task_save")
        
        app.start()

        assert task_save_mock.called


    @pytest.mark.parametrize("user_choice", [MenuEnum.DECRYPT], indirect=True)
    def test_start_should_invoke_task_decrypt_from_tasks_dict_when_user_chose_menu_enum_decrypt(self,
        while_loop_iteration_control, app, user_choice):
        task_decrypt_mock = app.tasks[MenuEnum.DECRYPT] = Mock(name="task_decrypt")
        
        app.start()

        assert task_decrypt_mock.called


    @pytest.mark.parametrize("user_choice", [MenuEnum.PEEK], indirect=True)
    def test_start_should_invoke_task_peek_the_buffer_from_tasks_dict_when_user_chose_menu_enum_peek_the_buffer(self,
        while_loop_iteration_control, app, user_choice):
        task_peek_the_buffer_mock = app.tasks[MenuEnum.PEEK] = Mock(name="task_peek_the_buffer")
        
        app.start()

        assert task_peek_the_buffer_mock.called


    def test_start_should_invoke_task_exit_from_tasks_dict_when_user_chose_interrupt_option(self,
        mocker, while_loop_iteration_control, app):
        mocker.patch("application.ciphering.Ciphering._Ciphering__get_user_choice", return_value=app.interrupt_option)
        task_exit_mock = app.tasks[app.interrupt_option] = Mock(name="task_exit")
        
        app.start()

        assert task_exit_mock.called


    def test_start_should_invoke_get_user_choice_of_self_again_when_user_type_nonexisted_option(self,
        mocker, app):
        choices = ["test", 100, app.interrupt_option]
        get_user_choice_mock = mocker.patch("application.ciphering.Ciphering._Ciphering__get_user_choice",
            side_effect=choices)

        app.start()
 
        assert len(choices) == len(get_user_choice_mock.mock_calls)


    def test_task_encrypt_should_invoke_get_user_choice_of_self_again_when_user_type_nonexisted_option(self,
        mocker, app):
        return_value = len(app.coders) + 1
        choices = ["test", 100, return_value]
        get_user_choice_mock = mocker.patch("application.ciphering.Ciphering._Ciphering__get_user_choice",
            side_effect=choices)

        app._Ciphering__task_encrypt()

        assert len(choices) == len(get_user_choice_mock.mock_calls)


    @pytest.mark.parametrize("user_choice", [1, 2, "1", "anything"], indirect=True)
    def test_task_encrypt_should_invoke_buffer_creator_of_self_when_user_choose_anything_except_return_option(self,
        mocker, user_choice, app, coder_mock, input_mock, get_coder_name_mock, buffer_creator_mock):
        app._Ciphering__task_encrypt()

        assert buffer_creator_mock.called


    @pytest.mark.parametrize("user_choice", [1, 2, "1", "anything"], indirect=True)
    def test_task_encrypt_should_invoke_encode_of_coder_when_user_choose_anything_except_return_option(self,
        mocker, user_choice, app, coder_mock, input_mock, get_coder_name_mock, buffer_creator_mock):
        app._Ciphering__task_encrypt()

        assert coder_mock.encode.called


    @pytest.mark.parametrize("user_choice", [1, 2, "1", "anything"], indirect=True)
    def test_task_encrypt_should_invoke_get_coder_name_of_self_when_user_choose_anything_except_return_option(self,
        mocker, user_choice, app, coder_getter_mock, input_mock, get_coder_name_mock, buffer_creator_mock):
        app._Ciphering__task_encrypt()

        assert get_coder_name_mock.called

    
    def test_task_encrypt_should_return_none_when_user_choice_is_len_coders_increased_by_one(self, mocker, app):
        user_choice = len(app.coders) + 1
        mocker.patch("application.ciphering.Ciphering._Ciphering__get_user_choice", return_value=user_choice)

        result = app._Ciphering__task_encrypt()

        assert result == None


    def test_task_save_to_file_should_set_buffer_to_none_after_save_of_file(self,
        app, file_manager_mock, input_mock, set_buffer_attribute):
        app._Ciphering__task_save_to_file()
        assert app.buffer == None


    def test_task_save_to_file_should_invoke_save_method_of_file_manager(self,
        mocker, app, file_manager_mock, input_mock, set_buffer_attribute):
        app._Ciphering__task_save_to_file()

        assert file_manager_mock.save.called


    def test_task_save_to_file_should_return_none_when_buffer_is_empty(self, app):
        app.buffer = None
        result = app._Ciphering__task_save_to_file()

        assert result == None


    def test_task_decrypt_should_invoke_methods_in_correct_order(self,
        app, file_manager_mock, coder_getter_mock, coder_mock, file_data, os_listdir_mock, input_mock):
        counter = Mock()
        counter.attach_mock(file_manager_mock, "file_manager")
        counter.attach_mock(coder_getter_mock, "get_coder")
        counter.attach_mock(coder_mock, "coder")

        coder = file_data["coder"]
        text = file_data["text"]

        order = [call.file_manager.read(input_mock), call.get_coder(coder), call.coder.decode(text)]

        app._Ciphering__task_decrypt()

        assert counter.method_calls == order


    def test_task_decrypt_should_return_none_when_file_name_was_typed_improperly(self,
        mocker, app, file_manager_mock, input_mock):
        mocker.patch("application.ciphering.os.listdir", return_value=["improperly-test-file"])
        result = app._Ciphering__task_decrypt()

        assert result == None


    def test_task_decrypt_should_invoke_decode_method_of_coder_when_file_name_was_typed_properly(self,
        app, file_manager_mock, input_mock, os_listdir_mock, coder_mock):
        app._Ciphering__task_decrypt()

        assert coder_mock.decode.called


    def test_task_decrypt_should_invoke_get_coder_method_of_self_when_file_name_was_typed_properly(self,
        app, file_manager_mock, input_mock, os_listdir_mock, coder_getter_mock):
        app._Ciphering__task_decrypt()

        assert coder_getter_mock.called


    def test_task_decrypt_should_invoke_read_method_of_file_manager_when_file_name_was_typed_properly(self,
        app, file_manager_mock, input_mock, os_listdir_mock):
        app._Ciphering__task_decrypt()

        assert file_manager_mock.read.called


    def test_task_decrypt_should_return_none_when_dir_with_files_is_empty(self, mocker, app, file_manager_mock):
        mocker.patch("application.ciphering.os.listdir", return_value=[])
        result = app._Ciphering__task_decrypt()

        assert result == None


    def test_get_user_choice_should_return_str_type_when_letters_provided_to_input(self, app, input_mock):
        result = app._Ciphering__get_user_choice()

        assert isinstance(result, str)


    def test_get_user_choice_should_return_int_type_when_number_provided_to_input(self, mocker, app):
        mocker.patch("application.ciphering.input", return_value="123")
        result = app._Ciphering__get_user_choice()

        assert isinstance(result, int)


    def test_get_coder_should_return_coder_instance(self, app):
        instance = app._Ciphering__get_coder(app.coders[1])

        assert isinstance(instance, Coder)


    def test_get_file_manager_should_return_file_manager_instance(self, app):
        instance = app._Ciphering__get_file_manager(app.file_manager_name)

        assert isinstance(instance, FileManager)


    def test_get_coder_should_invoke_get_coder_of_coder_factory(self, mocker, app):
        get_coder_mock = mocker.patch("application.ciphering.CoderFactory.get_coder")
        app._Ciphering__get_coder("coder_name")

        assert get_coder_mock.called


    def test_get_file_manager_should_invoke_get_file_manager_of_file_manager_factory(self, mocker, app):
        get_file_manager_mock = mocker.patch("application.ciphering.FileManagerFactory.get_file_manager")
        app._Ciphering__get_file_manager("file_manager_name")

        assert get_file_manager_mock.called
