import requests


def home_api(params=None, id=None):
    if id == None:
        url = "https://rawg-video-games-database.p.rapidapi.com/games?key=ad7b3c271f374cc5b44fc2ece596f911"
    else:
        url = "https://rawg-video-games-database.p.rapidapi.com/games/{id}?key=ad7b3c271f374cc5b44fc2ece596f911".format(
            id=id
        )
    headers = {
        "X-RapidAPI-Key": "c88f979badmsh9662554058f1528p101e76jsnf3faca908bec",
        "X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com",
    }
    if params != None:
        response = requests.request("GET", url, headers=headers, params=params)
    else:
        response = requests.request("GET", url, headers=headers)
    return response
