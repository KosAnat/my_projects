from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = "6018984602:AAFL_Cnkz3iCKuvatQF0jj3XwlhuF1qcOMU"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
