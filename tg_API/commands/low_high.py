from typing import List
from telebot.types import Message, InputMediaPhoto

from database.common.models import db, History
from database.core import db_write
from ..core import bot
from ..utils import constants
from site_API.api_request import api_request


def user_choice_city(message: Message) -> None:
    if message.text == '/low':
        ordering = 'ascending'
    else:
        ordering = 'descending'

    msg = bot.send_message(message.from_user.id, constants.CITY)
    bot.register_next_step_handler(msg, unit_quantity, ordering)


def unit_quantity(message: Message, ordering: str) -> None:
    city = message.text

    msg = bot.send_message(message.from_user.id, constants.UNITS)
    bot.register_next_step_handler(msg, present_property, ordering, city)


def present_property(message: Message, ordering: str, city: str) -> None:
    units = int(message.text)

    if units > 40:
        bot.send_message(message.from_user.id, "The number of apartments should be no more than 40")
        bot.register_next_step_handler("Enter the quantity: ", unit_quantity)

    else:
        user_id = message.from_user.id

        try:
            data = api_request.request_from_user(city, ordering, units, user_id)

            bot.send_message(message.from_user.id, f'Results for your request: ')

            if len(data) >= units:
                for i in range(units):
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

            else:
                for i in range(len(data)):
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

        except Exception:
            bot.send_message(message.from_user.id, constants.ERROR_MESSAGE)


def send_photo(photo_url: str) -> List:
    list_of_urls = [
        photo_url
    ]
    media_group = []

    for number, url in enumerate(list_of_urls):
        media_group.append(InputMediaPhoto(media=url, caption=f"Photo"))

    return media_group
