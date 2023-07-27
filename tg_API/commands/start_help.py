from telebot.types import Message

from ..core import bot
from ..utils import constants
from . import low_high, custom, history


@bot.message_handler(commands=constants.COMMAND)
def start_command(message: Message) -> None:
    if message.text == constants.START:
        bot.send_message(message.from_user.id, constants.WELCOME.format(message.from_user.first_name))
        bot.send_message(message.from_user.id, constants.INSTRUCTION)
    elif message.text == constants.HELP:
        bot.send_message(message.from_user.id, constants.HELP_MESSAGE)
    elif message.text in [constants.LOW, constants.HIGH]:
        low_high.user_choice_city(message)
    elif message.text == constants.CUSTOM:
        custom.user_choice_city(message)
    elif message.text == constants.HISTORY:
        history.history(message)
    else:
        bot.send_message(message.from_user.id, constants.HELP_MESSAGE)
