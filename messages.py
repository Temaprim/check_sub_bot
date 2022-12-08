import database
import config


# Думали с заказчицей какой формат для ссылок на каналы сделать, ей понравились
# обычные ссылки через перевод строки. Ну ладно. 
# Ещё больше дробить не захотел, запихнул в одну функцию
def get_channel_list_string(path: str) -> str:
    db = database.get_csv_db(path)

    channel_list_string = ''
    for channel in db:
        link = channel['invite_link']
        text = channel['name']
        channel_list_string += f'<a href="{link}">{text}</a>\n'

    return channel_list_string


channel_list_string = get_channel_list_string(config.DATABASE_PATH)

HELLO = (
        'Привет, {}!\n\n'
        'Я бот-помощник <a href="https://t.me/marafon_telega">'
        'марафона-практикума «Телега знаний»</a>\n\n '
        'Чтобы получить все подарки и бонусы от спикеров и '
        'марафона - нужно подписаться на все каналы спикеров и марафона🔻\n\n'
        f'{channel_list_string}\n'
        'Если все сделал(а) правильно, то нажимай кнопку «Получить подарки🎁»'
    )

CHECK_ERROR = (
        "Ой, проверь ещё раз все подписки на каналы внимательно и "
        "сможешь получить свои подарки 😉"
    )

AFTER_CHECK_ERROR = (
        f'{channel_list_string}\n'  
        'Проверь ещё раз свои подписки и жми «Подписан(а) на всех ✅'
    )

AFTER_CHECK_SUCCESS = (
        'Ура, ты подписался на всех!\n\n'
        'Нажимай «Получить подарки 🎁»'
    )

