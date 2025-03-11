import json

from . import global_def

normal_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 
                56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77]
special_drawables = [79, 44, 46, 48, 42, 52, 53, 54, 43, 45, 51, 80, 31]

class Card:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


def load_card_from_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    cards = {}
    for key, value in json_data.items():
        if value.get("weight") == 0:
            continue
        
        card = Card(id=value["id"], name=value["name"], description = value["description"])
        cards[str(key)] = card

    return cards


def load_cards():
    if global_def.all_cards_loaded:
        return

    global_def.all_cards = load_card_from_json(global_def.CARD_JSON_PATH)
    global_def.all_cards_loaded = True


def find_card_by_id(id: str) -> Card:
    load_cards()

    return global_def.all_cards.get(str(id))