import json

import pygame as pg
from random import choice

pg.init()
font = pg.font.Font(None, 40)
font_mini = pg.font.Font(None, 15)
font_maxi = pg.font.Font(None, 200)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text, text_font=font):
    return text_font.render(str(text), True, "black")


def get_random_item(items: list):
    return choice(items)


def read_json(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def change_data(game):
    data = {
        "happiness": game.happiness,
        "satiety": game.satiety,
        "health": game.health,
        "money": game.money,
        "coins_per_second": game.coins_per_second,
        "costs_of_upgrade": {
            "100": game.costs_of_upgrade[100],
            "1000": game.costs_of_upgrade[1000],
            "5000": game.costs_of_upgrade[5000],
            "10000": game.costs_of_upgrade[10000]
        },
        "clothes": []
    }

    for item in game.clothes_menu.items:
        data["clothes"].append(
            {
                "name": item.name,
                "price": item.price,
                "image": item.file,
                "is_bought": item.is_bought,
                "is_using": item.is_using,
            }
        )
    return data
