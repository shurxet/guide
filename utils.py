import json

from itertools import compress
from pprint import pprint
from typing import Generator

path = 'data.json'


def get_data() -> dict[list[dict[int, str, str, str, str, str, str]]]:
    """
    The get_data() function opens a json file, retrieves data from it, and returns a dict
    :return:  -> dict[list[dict[int, str, str, str, str, str, str]]]
    """
    with open(path, 'r', encoding='utf-8') as f:
        data: dict[list[dict[int, str, str, str, str, str, str]]] = json.load(f)
    return data


def portions_data() -> Generator | dict[str, set[Exception]]:
    """
    The portions_data() function opens a json file and uses a generator to return data in parts, saving RAM resources in
    cases where there will be a lot of data, as well as this function handles possible errors and the program continues
    to work
    :return: -> Generator | dict[str, set[Exception]]
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data: dict = json.load(f)
        while True:
            yield from data["list_contacts"]
    except Exception as e:
        return {"Что-то пошло не так": {e}}


def save_data(data: dict | list[dict[int, str, str, str, str, str, str]]) -> dict[str, set[Exception]]:
    """
    The save_data() function accepts new or updated dict data, saves it in a json file, and also handles possible errors
    and the program continues to work further
    :param data: save_data(data: dict | list[dict[int, str, str, str, str, str, str]])
    :return: -> dict[str, set[Exception]]
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return {"Что-то пошло не так": {e}}


def get_new_id() -> int:
    """
    The get_new_id() function generates a new record id and returns an int
    :return: -> int
    """
    new_id: int = 1
    data: dict = get_data()
    result: int = max(list(map(lambda x: x['id'], data["list_contacts"])))
    new_id += result

    return new_id


def add_data() -> dict[int, str, str, str, str, str, str] | dict[str, set[Exception]]:
    """
    The add_data() function processes the new received data, generates the data in dict and adds it to a json file,
    passes the data to the save_data() function for processing to write to a json file and gives the new data to dict,
    as well as handles possible errors and the program continues to work further
    :return: -> dict[int, str, str, str, str, str, str] | dict[str, set[Exception]]
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
        record_id: int = get_new_id()
        new_data['id']: int = record_id
        for key, value in new_data.items():
            if key != 'id':
                user_input: str = str(input(f'{key}:\n'))
                new_data[key] = user_input
        data: dict = get_data()
        data["list_contacts"].append(new_data)
        save_data(data)
        return new_data
    except Exception as e:
        return {"Что-то пошло не так": {e}}


def edit_data() -> dict[int, str, str, str, str, str, str] | dict[str, set[Exception]]:
    """
    The edit_data() function gets the necessary record by ID, updates the data in this record and returns the updated
    dict data, it also handles possible errors, and the program continues to work further
    :return: -> dict[int, str, str, str, str, str, str] | dict[str, set[Exception]]
    """
    try:
        user_input: int = int(input('введите id редактируемой записи:\n'))
        data: dict = get_data()
        items_bool: list = list(map(lambda x: x["id"] == user_input, data["list_contacts"]))
        update_data: dict = list(compress(data["list_contacts"], items_bool))[0]
        pprint(update_data)
        for key, value in update_data.items():
            if key != 'id':
                user_input: str = str(input(f'Редакировать {key} (if yes press y/default no, press the enter key): '))
                if user_input.lower() == 'y':
                    user_input: str = str(input(f'{key}: '))
                    update_data[key]: str = user_input
        save_data(data)
        return update_data
    except Exception as e:
        return {"Что-то пошло не так": {e}}


def by_id() -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[Exception]]:
    """
    The by_id() function searches for a record by id and returns the found record dict it also handles possible errors,
    and the program continues to work further
    :return: -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[Exception]]
    """
    try:
        user_input: int = int(input('введите id: \n'))
        data: dict = get_data()
        items_bool: list = list(map(lambda x: user_input == x["id"], data["list_contacts"]))
        data_filter: list = list(compress(data["list_contacts"], items_bool))
        if len(data_filter) < 1:
            data_filter.append('записей не найдено')

        return data_filter
    except Exception as e:
        return {"Что-то пошло не так": {e}}


def by_last_name() -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[Exception]]:
    """
    The by_last_name() function searches for a record by last_name and returns the found record, it also handles
    possible errors, and the program continues to work further
    :return: -> list[dict[int, str, str, str, str, str, str]] | list[str] | dict[str, set[Exception]]
    """
    user_input: str = str(input('введите last_name: \n'))
    data: dict = get_data()
    items_bool: list = list(map(lambda x: user_input == x["last_name"], data["list_contacts"]))
    data_filter: list = list(compress(data["list_contacts"], items_bool))
    if len(data_filter) < 1:
        data_filter.append('записей не найдено')

    return data_filter
