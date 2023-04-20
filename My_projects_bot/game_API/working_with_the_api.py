import requests

from game_API import home_API


def search_game(query: str, flag=False) -> str:
    """
    Данная функция ищет игры, выдает списох подходящих по названию игр. А также, с помощью параметра 'flag',
    помогает функции all_about_game, находить полную иформацию по названию игры, а не по ее id.
    :param query: Название игры
    :param flag: Переключатель, который используется в функции "all_about_game", для более правильной и
    красивой работы.
    :return:Возвращает название игр или id игры, в зависимости от flag.
    """
    try:
        params = {"search": query, "page": 1, "page_size": 20}
        response = home_API.home_api(params=params)
        if response.status_code == 200:
            games = response.json()["results"]
            for game in games:
                if flag == False:
                    yield "{name}".format(name=game["name"])
                else:
                    yield game["id"]
        else:
            yield "Данной игры не существует."
    except ValueError:
        yield "Ввод некорректен, попробуйте еще раз"


def all_about_game(name: str) -> str:
    """
    Данная функция находит полную информацию о игре и возвращает ее. Поиск проходит с использованием функции search_game
    и id, который она возвращает.
    :param name:Название игры
    :return:Подробная информация о игре
    """
    try:
        first_id = next(search_game(query=name, flag=True))
        response = home_API.home_api(id=str(first_id))

        if response.status_code == 200:
            games = response.json()
            platforms_list = [i["platform"]["name"] for i in games["platforms"]]
            platforms = ""

            for i in platforms_list:
                platforms += i + ". "

            return (
                'Название: {name}\n\nДата выпуска: {released}\n\nРейтинг по версии "metacritic": {metacritic}\n\nПримерное время прохождения игры: '
                "{playtime} часа\n\nИгровые платформы: {platforms}\n\nОфициальный сайт игры: {website}".format(
                    name=games["name"],
                    website=games["website"],
                    playtime=games["playtime"],
                    released=games["released"],
                    platforms=platforms,
                    metacritic=games["metacritic"],
                )
            )
    except ValueError:
        return "Ввод некорректен, попробуйте еще раз"


def low_high(query: str, count: str, flag=True) -> str:
    """
    Данная функция возвращает игры, исходя из их рейтинга по "metacritic". В большую сторону или меньшую в зависимости
    от того, что захочет пользователь.(flag = True or flag = False)
    :param query: число, от которого должен начинаться поиск
    :param count: количество игр, которое должно быть выведено
    :param flag: от этого зависит в большую или меньшую сторону будет проходить поиск
    :return: игры(название, рейтинг)
    """
    try:
        if 10 <= int(query) <= 100 and int(count) > 0:
            if flag == True:
                ordering = "metacritic"
                query += ",100"
            else:
                ordering = "-metacritic"
                query = "10," + query

            params = {
                "metacritic": query,
                "page": 1,
                "page_size": int(count),
                "ordering": ordering,
            }
            response = home_API.home_api(params=params)

            if response.status_code == 200:
                games = response.json()["results"]
                for game in games:
                    yield "Название: {name} - Рейтинг: {metacritic}".format(
                        name=game["name"], metacritic=game["metacritic"]
                    )
        else:
            yield "Ввод некорректен, попробуйте еще раз"
    except ValueError:
        yield "Ввод некорректен, попробуйте еще раз"


def range_game(query: str, count: str) -> str:
    """
    Функция схожа с предыдущей, но без параметра 'flag'. Она возвращает игры, исходя из их рейтинга по "metacritic". В диапозоне в зависимости
    от того, что захочет пользователь.
    :param query: Диапозон: 40,60
    :param count: Количество игр, которых необходимо вывести
    :return: игры(название, рейтинг)
    """
    try:
        if int(count) > 0:
            params = {
                "metacritic": query,
                "page": 1,
                "page_size": int(count),
                "ordering": "metacritic",
            }
            response = home_API.home_api(params=params)

            if response.status_code == 200:
                games = response.json()["results"]
                for game in games:
                    yield "Название: {name} - Рейтинг: {metacritic}".format(
                        name=game["name"], metacritic=game["metacritic"]
                    )
        else:
            yield "Ввод некорректен, попробуйте еще раз"
    except ValueError:
        yield "Ввод некорректен, попробуйте еще раз"
