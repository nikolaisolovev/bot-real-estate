from typing import List
from telebot.types import Message, InputMediaPhoto

from database.common.models import db, History
from database.core import db_write
from ..core import bot
from ..utils import constants
from site_API.api_request import api_request


def user_choice_city(message: Message) -> None:
    msg = bot.send_message(message.from_user.id, constants.CITY)
    bot.register_next_step_handler(msg, user_choice_min_value)


def user_choice_min_value(message: Message) -> None:
    city = message.text

    msg = bot.send_message(message.from_user.id, constants.MIN_VALUE)
    bot.register_next_step_handler(msg, user_choice_max_value, city)


def user_choice_max_value(message: Message, city: str) -> None:
    min_value = int(message.text)

    msg = bot.send_message(message.from_user.id, constants.MAX_VALUE)
    bot.register_next_step_handler(msg, unit_quantity, city, min_value)


def unit_quantity(message: Message, city: str, min_value: int) -> None:
    max_value = int(message.text)

    msg = bot.send_message(message.from_user.id, constants.UNITS)
    bot.register_next_step_handler(msg, present_property, city, min_value, max_value)


def present_property(message: Message, city: str, min_value: int, max_value) -> None:
    units = int(message.text)
    user_id = message.from_user.id

    try:
        data = api_request.custom_request_from_user(city, min_value, max_value, units, user_id)

        bot.send_message(message.from_user.id, f'Results for your request: ')

        if len(data) >= units:
            for i in range(units):
                write_to_db_and_send_message(city, data, i, message)

        else:
            for i in range(len(data)):
                write_to_db_and_send_message(city, data, i, message)

    except Exception:
        print('Error Exception')
        bot.send_message(message.from_user.id, constants.ERROR_MESSAGE)


def write_to_db_and_send_message(city, data, i, message):
    data_dict = data[i]
    photo = data_dict["photo"]
    db_write(db, History, data_dict)
    result_message = f"\nCity: {city}" \
                     f"\nCounty: {data_dict['county']}" \
                     f"\nMonthly rent: {data_dict['price']}" \
                     f"\nAddress: {data_dict['address']}" \
                     f"\nURL for details: {data_dict['url']}"
    bot.send_message(message.from_user.id, result_message)
    bot.send_media_group(message.from_user.id, media=send_photo(photo))


def send_photo(photo_url: str) -> List:
    list_of_urls = [
        photo_url
    ]
    media_group = []

    for number, url in enumerate(list_of_urls):
        media_group.append(InputMediaPhoto(media=url, caption=f"Photo"))

    return media_group
