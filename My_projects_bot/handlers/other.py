import json
import string

from aiogram import Dispatcher, types

from create_bot import dp


async def swearing(message: types.Message):
    """Данная функция удаляет мат, который схож с теми словами ,которые находятся в файле "cenz.json"
    и делает замечание
    """
    word = {
        i.lower().translate(str.maketrans("", "", string.punctuation))
        for i in message.text.split(" ")
    }.intersection(set(json.load(open("cenz.json"))))
    if word != set():
        await message.reply("Мат запрещен!")
        await message.delete()


def register_handers_other(dp: Dispatcher):
    dp.register_message_handler(swearing)
