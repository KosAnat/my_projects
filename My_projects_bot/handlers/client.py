import sqlite3

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, dp
from data_base import sqlite_db
from game_API import working_with_the_api
from keyboards import kb_client


async def send_welcome(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            "Привет!\nЯ GameBot!\nЯ выдаю подробную информацию о необходимой игре, а также провожу "
            "поиски по играм.\nДля более подробной информации нажми кнопку или введи команду: "
            "<b>\help</b>",
            reply_markup=kb_client,
            parse_mode="html",
        )
        await message.delete()
    except:
        await message.reply(
            "Общение с ботом через лс, напишите ему:\nhttps://t.me/All_about_game_bot"
        )


class FSM_all_game(StatesGroup):
    searching_game = State()

    info_game = State()

    high_1 = State()
    high_2 = State()

    low_1 = State()
    low_2 = State()

    range_game_1 = State()
    range_game_2 = State()


async def all_game(message: types.Message):
    """
    Данная функция заправшивает у пользователя название игры или часть названия игры и вводит бота в машину состояний.
    :param message: Сообщение от пользователя
    :return: Запрос на ввод игры
    """
    sqlite_db.add_history_record(message.from_user.id, message.text)
    await FSM_all_game.searching_game.set()
    await message.reply(
        "Введите игру или часть названия игры, чтобы найти ее полное название\nНапример:\nВы хотите найти игру Grand Theft Auto V."
        " Отправьте: Grand\nИ бот обязательно отправит вам список игр, которые начинаются на 'Grand'!"
    )


async def search_and_send_game(message: types.Message, state: FSMContext):
    """Отлавливает сообщение пользователя, после ввода выводит список подходящих по поиску игр"""
    for game in working_with_the_api.search_game(message.text):
        await bot.send_message(message.from_user.id, game)
    await message.reply("Поиск завершен")

    await state.finish()


async def full_game(message: types.Message):
    """Запрашивает у пользователя название игры, чтобы выловить сообщение и вывести более подробную информацию и
    вводит бота в машину состояний"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    await FSM_all_game.info_game.set()
    await message.reply(
        "Введите название игры, о которой хотите получить полную информацию"
    )


async def info_game(message: types.Message, state: FSMContext):
    """Отлавливает сообщение и  выводит полную информацию о игре"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    game = working_with_the_api.all_about_game(message.text)
    await bot.send_message(message.from_user.id, game)

    await state.finish()


async def high(message: types.Message):
    """Данная функция запрашивает у пользователя рейтинг, от которых необходимо начать поиск, а также вводит бота в машину состояний"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    await FSM_all_game.high_1.set()
    await message.reply(
        'Поиск по рейтингу "metacritic"\nВведите рейтинг от 10 до 100, от которого необходимо начать поиск '
        "в сторону более высокого рейтинга\nНапример: 40"
    )


async def high_metacritic(message: types.Message, state: FSMContext):
    """Данная функция улавливает сообщение от пользователя, добавляет его в словарь 'data',
    после запрашивает количество игр и с помощью FSM_all_game.next()  - переводит пользователя далее
    """
    sqlite_db.add_history_record(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["high_metacritic"] = message.text
    await FSM_all_game.next()
    await message.reply("Введите количество игр, которое хотите увидеть:")


async def high_count(message: types.Message, state: FSMContext):
    """Данная функция улавливает сообщение от пользователя добавляет его в словарь 'data', после выдает необходимый список"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["high_count"] = message.text
    for game in working_with_the_api.low_high(
        query=data["high_metacritic"], count=data["high_count"]
    ):
        await bot.send_message(message.from_user.id, game)
    await message.reply("Поиск завершен")
    await state.finish()


async def low(message: types.Message):
    """Данная функция запрашивает у пользователя рейтинг, от которых необходимо начать поиск, а также вводит бота
    в машину состояний"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    await FSM_all_game.low_1.set()
    await message.reply(
        'Поиск по рейтингу "metacritic"\nВведите рейтинг от 10 до 100, от которого необходимо начать поиск '
        "в сторону меньшего рейтинга\nНапример: 40"
    )


async def low_metacritic(message: types.Message, state: FSMContext):
    """Данная функция улавливает сообщение от пользователя, добавляет его в словарь 'data',
    после запрашивает количество игр и с помощью FSM_all_game.next()  - переводит пользователя далее
    """
    sqlite_db.add_history_record(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["low_metacritic"] = message.text
    await FSM_all_game.next()
    await message.reply("Введите количество игр, которое хотите увидеть:")


async def low_count(message: types.Message, state: FSMContext):
    """Данная функция запрашивает у пользователя рейтинг, от которых необходимо начать поиск, а также вводит бота
    в машину состояний"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["low_count"] = message.text
    for game in working_with_the_api.low_high(
        query=data["low_metacritic"], count=data["low_count"], flag=False
    ):
        await bot.send_message(message.from_user.id, game)
    await message.reply("Поиск завершен")
    await state.finish()


async def range(message: types.Message):
    """Данная функция запрашивает у пользователя диапазон рейтинга, а также вводит бота в машину состояний"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    await FSM_all_game.range_game_1.set()
    await message.reply(
        'Поиск по рейтингу "metacritic"\nВведите рейтинг от 10 до 100, через запятую, от меньшего к большему.  '
        "\nНапример: 20,40\nБот выдаст вам список игр в этом диапазоне "
    )


async def range_metacritic(message: types.Message, state: FSMContext):
    """Данная функция улавливает сообщение от пользователя, добавляет его в словарь 'data',
    после запрашивает количество игр и с помощью FSM_all_game.next()  - переводит пользователя далее
    """
    sqlite_db.add_history_record(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["range_metacritic"] = message.text
    await FSM_all_game.next()
    await message.reply("Введите количество игр, которое хотите увидеть:")


async def range_game_count(message: types.Message, state: FSMContext):
    """Данная функция улавливает сообщение от пользователя , после выдает необходимый список"""
    sqlite_db.add_history_record(message.from_user.id, message.text)
    async with state.proxy() as data:
        data["range_game_count"] = message.text
    for game in working_with_the_api.range_game(
        query=data["range_metacritic"], count=data["range_game_count"]
    ):
        await bot.send_message(message.from_user.id, game)
    await message.reply("Поиск завершен")
    await state.finish()


async def history_command_handler(message: types.Message):
    """Данная функция"""
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        "SELECT query FROM history WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
        (message.from_user.id,),
    )
    rows = c.fetchall()
    conn.close()

    if rows:
        responce = "Последние 10 запросов:\n\n"
        for row in rows:
            responce += "- {row}\n\n".format(row=row[0])
    else:
        responce = "Вы еще не сделали ни одного запроса"
    await message.answer(responce)


async def helper(message: types.Message):
    sqlite_db.add_history_record(message.from_user.id, message.text)
    await message.answer(
        "Команда <b>/Найти_игру</b>:"
        "\nДанная команда запрашивает у вас название игры или ее часть, после чего выдает "
        "список из игр с похожим названием, которое должно вам подойти!\n\n"
        "Команда <b>/custom</b>:\n"
        "Данная команда запрашивает у вас название игры, после чего выводит более подробную информацию\n\n"
        "Команда <b>/high</b>:\n"
        'Данная команда проводит поиск по рейтингу "metacritic" в большую сторону. Например: вы вводите рейтинг '
        "40, вам выдаются игры с рейтингом 40 и выше\n\n"
        "Команда <b>/low</b>:\n"
        'Данная команда проводит поиск по рейтингу "metacritic" в меньшую сторону. Например: вы вводите рейтинг '
        "40, вам выдаются игры с рейтингом 40 и ниже\n\n"
        "Команда <b>/range</b>:\n"
        'Данная команда проводит поиск по рейтингу "metacritic" в диапазоне. Например: вы вводите рейтинг '
        "40,60(через запятую), вам выдаются игры с рейтингом от 40 до 60 \n\n"
        "Команда <b>/history</b>:\n"
        "Данная команда выдает последние 10 запросов, которые вы вводили(если такие имеются) \n\n"
        "Команда <b>/help</b>:\n"
        "Данная команда выдает информацию о всех командах",
        parse_mode="html",
    )


async def the_сomands_does_not_exist(message: types.Message):
    await message.reply("Данной команды не существует")


def register_handers_client(dp: Dispatcher):
    commands_with_none = [
        (["start"], send_welcome),
        (["Найти_игру"], all_game),
        (["custom"], full_game),
        (["high"], high),
        (["low"], low),
        (["range"], range),
        (["history"], history_command_handler),
        (["help"], helper),
        (None, the_сomands_does_not_exist),
    ]

    commands_2 = [
        (search_and_send_game, FSM_all_game.searching_game),
        (high_metacritic, FSM_all_game.high_1),
        (high_count, FSM_all_game.high_2),
        (low_metacritic, FSM_all_game.low_1),
        (low_count, FSM_all_game.low_2),
        (range_metacritic, FSM_all_game.range_game_1),
        (range_game_count, FSM_all_game.range_game_2),
        (info_game, FSM_all_game.info_game),
    ]

    for i in commands_with_none:
        dp.register_message_handler(i[1], commands=i[0], state=None)

    for i in commands_2:
        dp.register_message_handler(i[0], state=i[1])
