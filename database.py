import csv
import sys
import logging
import os


DATABASE_ERROR_MESSAGE = (
    'Проблемы с базой данных.\n'
    'Причины ошибки:\n'
    ' - Файл базы данных не обнаружен\n'
    ' - Названия столбцов не соответствуют норме - '
    '"name", "invite_link", "channel_id"\n'
    ' - Не все ячейки в таблице заполнены\n'
    ' - Айди канала должен быть записан числом (например, "-100200300400")'
)


# str.isdigit() не подходит,
# он кидает False на проверку отрицательных чисел. Написал свой, железобетонный
def isint(obj: str) -> bool:
    try: 
        int(obj)
        return True
    except ValueError:
        return False


# Личный запрос заказчика, чтобы бд была в csv. Ну, как хочет.
#
# Структура следующая: 
# | name |       invite_link       |   channel_id   |
# | Вася | https://t.me/канал_васи | -1005002281337 |
#
# Ниже проверка на нежданчики.
def is_database_correct(path: str) -> bool:
    if not os.path.isfile(path):
        return False

    with open(path) as csv_base:
        base = csv.DictReader(csv_base)
        # Проходимся по итератору и получаем лист. 
        # База не должна быть слишком большой, 
        # так что на производительность чхать.
        base = list(base)  

        # Пуста ли база?
        if len(base) == 0:
            return False

        # Проверка названий столбцов
        if set(base[0].keys()) != {"name", "invite_link", "channel_id"}:
            return False
      
        for line in base:
            # Все ячейки должны быть заполнены
            if None in line.values() or '' in line.values():
                return False
            
            # Айди канала должно быть числом
            if not isint(line["channel_id"]):
                return False

    # Если всё ок
    return True

def validate_database(path: str) -> None:
    if not is_database_correct(path):
        logging.error(DATABASE_ERROR_MESSAGE)
        sys.exit(1)



def get_csv_db(path: str) -> list[dict]:
    validate_database(path)

    with open(path) as csv_file:
        db = csv.DictReader(csv_file)
        return list(db)

# Как избежать двойной валидации бд (в bot.py и в message.py) я так и 
# не придумал, надо будет как-то потыкаться. Но не велика потеря - база данных
# не должна быть больше 15-20 элементов

