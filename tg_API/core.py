import telebot

from settings import BotSettings


my_bot = BotSettings()
TOKEN = my_bot.bot_key.get_secret_value()

bot = telebot.TeleBot(token=TOKEN)
