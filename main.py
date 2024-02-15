from pprint import pprint
from typing import Generator

from utils import portions_data, add_data, edit_data, by_id, by_last_name


text_menu = (
    'Выберите нужный пункт меню:\n'
    'ENTER - смотреть/листать страницы справочника\n'
    '0 - завершить программу\n'
    '1 - добавить новую запись в справочник\n'
    '2 - редактировать запись в справочнике\n'
    '3 - поиск по id\n'
    '4 - поиск по last_name\n'
)


def main():
    """
    The main() function launches the main menu and depending on what the user chooses from the menu, the desired
    function imported from utils will be launched
    """
    data: Generator = portions_data()

    while True:
        user_input: str = str(input(text_menu))
        if user_input == '':
            pprint(next(data))
        elif user_input == '0':
            break
        elif user_input == '1':
            pprint(add_data())
        elif user_input == '2':
            pprint(edit_data())
        elif user_input == '3':
            pprint(by_id())
        elif user_input == '4':
            pprint(by_last_name())
        else:
            print('Нет такого пункта меню')


if __name__ == '__main__':
    main()
