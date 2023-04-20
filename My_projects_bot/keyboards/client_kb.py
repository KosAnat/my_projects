from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

key_board = ["/Найти_игру", "/custom", "/high", "/low", "/range", "/history", "/help"]

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

for i in key_board:
    kb_client.insert(i)
