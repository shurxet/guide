import json
from itertools import compress
from json import JSONDecodeError
from pprint import pprint
from typing import Generator


class Guide:
    """
    The Guide class implements the work of the entire program and has the following methods:
    1 ->    __init__(self, path_json: str):,
    2 ->    start(self) -> None,
    3 ->    start(self) -> None,
    4 ->    get_data(self) -> (dict[list[dict[int, str, str, str, str, str, str]]] | dict[str, FileNotFoundError] |
                           dict[str, JSONDecodeError]),
    5 ->    portions_data(self) -> Generator | dict[str, set[FileNotFoundError]] | dict[str, set[JSONDecodeError]],
    6 ->    save_data(self, data: dict | list[dict[int, str, str, str, str, str, str]]) -> (dict[str, FileNotFoundError] |
                                                                                        dict[str, JSONDecodeError]),
    7 ->    get_new_id(self) -> int,
    8 ->    add_data(self) -> dict[int, str, str, str, str, str, str] | dict[str, set[KeyError]],
    9 ->    edit_data(self) -> (dict[int, str, str, str, str, str, str] | dict[str, set[ValueError]] |
                            dict[str, set[KeyError]]),
   10 ->    by_id(self) -> (list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[ValueError]] |
                        dict[str, set[KeyError]]),
   11 ->    by_last_name(self) -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[KeyError]]
    """

    __text_menu = (
        'Выберите нужный пункт меню:\n'
        ' ENTER - смотреть/листать страницы справочника\n'
        '0 - завершить программу\n'
        '1 - добавить новую запись в справочник\n'
        '2 - редактировать запись в справочнике\n'
        '3 - поиск по id\n'
        '4 - поиск по last_name\n'
    )

    def __init__(self, path_json: str):
        self.path_json = path_json

    def start(self) -> None:
        """
        the start() function starts the main function with logic
        :return: -> None
        """
        self.logic_func(self.__text_menu)
        return self.logic_func(self.__text_menu)

    def logic_func(self, text) -> None:
        """
        The logic_funk() function launches a text menu, and depending on what the user selects in the menu, the desired
        function will be launched
        :return: -> None

        """
        data: Generator = self.portions_data()

        while True:
            user_input: str = str(input(text))
            if user_input == '':
                pprint(next(data))
            elif user_input == '0':
                break
            elif user_input == '1':
                pprint(self.add_data())
            elif user_input == '2':
                pprint(self.edit_data())
            elif user_input == '3':
                pprint(self.by_id())
            elif user_input == '4':
                pprint(self.by_last_name())
            else:
                pprint('Нет такого пункта меню')

    def get_data(self) -> (dict[list[dict[int, str, str, str, str, str, str]]] | dict[str, FileNotFoundError] |
                           dict[str, JSONDecodeError]):
        """
        The get_data() function opens a json file, retrieves data from it, and returns a dict, as well as this function
        handles possible errors and the program continues to work
        :return: -> dict[list[dict[int, str, str, str, str, str, str]]] | dict[str, FileNotFoundError] |
                     dict[str, JSONDecodeError]
        """
        try:
            with open(self.path_json, 'r', encoding='utf-8') as f:
                data: dict[list[dict[int, str, str, str, str, str, str]]] = json.load(f)
            return data
        except FileNotFoundError as e:
            return {'The file path is specified incorrectly': e}
        except JSONDecodeError as e:
            return {'Invalid JSON syntax': e}

    def portions_data(self) -> Generator | dict[str, set[FileNotFoundError]] | dict[str, set[JSONDecodeError]]:
        """
        The portions_data() function opens a json file and uses a generator to return data in parts, saving RAM
        resources in cases where there will be a lot of data, as well as this function handles possible errors and the
        program continues to work
        :return: -> Generator | dict[str, set[Exception]]
        """
        try:
            with open(self.path_json, 'r', encoding='utf-8') as f:
                data: dict = json.load(f)
            while True:
                yield from data["list_contacts"]
        except FileNotFoundError as e:
            return {'The file path is specified incorrectly': e}
        except JSONDecodeError as e:
            return {'Invalid JSON syntax': e}

    def save_data(self, data: dict | list[dict[int, str, str, str, str, str, str]]) -> (dict[str, FileNotFoundError] |
                                                                                        dict[str, JSONDecodeError]):
        """
        The save_data() function accepts new or updated dict data, saves it in a json file, and also handles possible
        errors and the program continues to work further
        :param data: save_data(data: dict | list[dict[int, str, str, str, str, str, str]])
        :return: -> dict[str, FileNotFoundError] | dict[str, JSONDecodeError]
        """
        try:
            with open(self.path_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            return {'The file path is specified incorrectly': e}
        except JSONDecodeError as e:
            return {'Invalid JSON syntax': e}

    def get_new_id(self) -> int:
        """
        The get_new_id() function generates a new record id and returns an int
        :return: -> int
        """
        new_id: int = 1
        data: dict = self.get_data()
        result: int = max(list(map(lambda x: x['id'], data["list_contacts"])))
        new_id += result

        return new_id

    def add_data(self) -> dict[int, str, str, str, str, str, str] | dict[str, set[KeyError]]:
        """
        The add_data() function processes the new received data, generates the data in dict and adds it to a json file,
        passes the data to the save_data() function for processing to write to a json file and gives the new data to
        dict, as well as handles possible errors and the program continues to work further
        :return: -> dict[int, str, str, str, str, str, str] | dict[str, set[KeyError]]
        """
        try:
            new_data: dict = {
                "id": int,
                "last_name": str,
                "first_name": str,
                "patronymic": str,
                "organization": str,
                "work_phone": str,
                "personal_phone": str
            }
            record_id: int = self.get_new_id()
            new_data['id']: int = record_id
            for key, value in new_data.items():
                if key != 'id':
                    user_input: str = str(input(f'{key}:\n'))
                    new_data[key] = user_input
            data: dict = self.get_data()
            data["list_contacts"].append(new_data)
            self.save_data(data)
            return new_data
        except KeyError as e:
            return {'Missing "list_contacts" key in JSON data': {e}}

    def edit_data(self) -> (dict[int, str, str, str, str, str, str] | dict[str, set[ValueError]] |
                            dict[str, set[KeyError]]):
        """
        The edit_data() function gets the necessary record by ID, updates the data in this record and returns the
        updated dict data, it also handles possible errors, and the program continues to work further
        :return: -> dict[int, str, str, str, str, str, str] | dict[str, set[ValueError]] | dict[str, set[KeyError]]
        """
        try:
            user_input: int = int(input('введите id редактируемой записи:\n'))
            data: dict = self.get_data()
            items_bool: list = list(map(lambda x: x["id"] == user_input, data["list_contacts"]))
            update_data: dict = list(compress(data["list_contacts"], items_bool))[0]
            pprint(update_data)
            for key, value in update_data.items():
                if key != 'id':
                    user_input: str = str(
                        input(f'Редакировать {key} (if yes press y/default no, press the enter key): '))
                    if user_input.lower() == 'y':
                        user_input: str = str(input(f'{key}: '))
                        update_data[key]: str = user_input
            self.save_data(data)
            return update_data
        except ValueError as e:
            return {'The value that the user passes must be an integer': {e}}
        except KeyError as e:
            return {'Missing "list_contacts" key in JSON data': {e}}

    def by_id(self) -> (list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[ValueError]] |
                        dict[str, set[KeyError]]):
        """
        The by_id() function searches for a record by id and returns the found record dict it also handles possible
        errors, and the program continues to work further
        :return: -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[ValueError]] |
                    dict[str, set[KeyError]]
        """
        try:
            user_input: int = int(input('введите id: \n'))
            data: dict = self.get_data()
            items_bool: list = list(map(lambda x: user_input == x["id"], data["list_contacts"]))
            data_filter: list = list(compress(data["list_contacts"], items_bool))
            if len(data_filter) < 1:
                data_filter.append('записей не найдено')
            return data_filter
        except ValueError as e:
            return {'The value that the user passes must be an integer': {e}}
        except KeyError as e:
            return {'Missing "list_contacts" key in JSON data': {e}}

    def by_last_name(self) -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[KeyError]]:
        """
        The by_last_name() function searches for a record by last_name and returns the found record, it also handles
        possible errors, and the program continues to work further
        :return: -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[Exception]]
        """
        try:
            user_input: str = str(input('введите last_name: \n'))
            data: dict = self.get_data()
            items_bool: list = list(map(lambda x: user_input == x["last_name"], data["list_contacts"]))
            data_filter: list = list(compress(data["list_contacts"], items_bool))
            if len(data_filter) < 1:
                data_filter.append('записей не найдено')
            return data_filter
        except KeyError as e:
            return {'Missing "list_contacts" key in JSON data': {e}}
