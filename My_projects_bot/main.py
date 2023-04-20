from aiogram import executor

from create_bot import dp
from data_base import sqlite_db


async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_db.sql_Start()


from handlers import client, other

client.register_handers_client(dp)
other.register_handers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
