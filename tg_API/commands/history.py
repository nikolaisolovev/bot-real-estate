from telebot.types import Message

from database.common.models import db, History
from database.core import db_read
from tg_API.core import bot


def history(message: Message) -> None:
    user_id = message.from_user.id
    retrieved = db_read(db, History, History.city, History.county, History.price, History.photo, id=user_id)
    bot.send_message(message.from_user.id, f'Ваши последние запросы:\n')

    for element in retrieved:
        photo = element.photo
        element = f'City: {element.city}\n' \
                  f'County: {element.county}\n' \
                  f'Price: {element.price}'

        bot.send_message(message.from_user.id, element)
        bot.send_photo(message.from_user.id, photo=photo)
