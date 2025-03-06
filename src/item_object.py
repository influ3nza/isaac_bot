import json
from nonebot import logger

from . import global_def

class Item:
    def __init__(self, id: int, name: str, aliases: list[str], description: str, labels_id: list[int], label_name: list[str], rarity: str, charge: str):
        self.id = id
        self.name = name
        self.aliases = aliases
        self.description = description
        self.labels_id = labels_id
        self.label_name = label_name
        self.rarity = rarity
        self.charge = charge


def load_items_from_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    items = {}
    for key, value in json_data.items():
        item = Item(id=value["id"], name=value["name"], aliases=value["aliases"], description = value["description"], labels_id=value["labels_id"], label_name=value["label_name"], rarity=value["rarity"], charge=value["charge"])
        items[key] = item
    return items


def load_items():
    if global_def.all_items_loaded:
        return

    global_def.all_items = load_items_from_json(global_def.ITEM_JSON_PATH)
    global_def.all_items_loaded = True


def find_item_by_id(item_id: int) -> Item:
    load_items()

    return global_def.all_items.get(str(item_id), None)


def find_items_by_name(search_string: str) -> list:
    load_items()

    matched_items = []
    for item in global_def.all_items.values():
        if search_string in item.name and not item in matched_items:
            matched_items.append(item)

    for item in global_def.all_items.values():
        for alias in item.aliases:
            if search_string in alias and not item in matched_items:
                matched_items.append(item)
    return matched_items


def find_items_by_name_strict(search_string: str) -> list:
    load_items()

    matched_items = []
    for item in global_def.all_items.values():
        if len(item.name) > 2:
            if len(search_string) > 2 and search_string in item.name and not item in matched_items:
                matched_items.append(item)
        else:
            if search_string in item.name and not item in matched_items:
                matched_items.append(item)
    
    for item in global_def.all_items.values():
        if search_string in item.aliases and not item in matched_items:
            matched_items.append(item)
    return matched_items


class Trinket:
    def __init__(self, id: int, name: str, description: str, aliases: list[str]):
        self.id = id
        self.name = name
        self.description = description
        self.aliases = aliases


def load_trinkets_from_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    trinkets = {}
    for key, value in json_data.items():
        trinket = Trinket(id=value["id"], name=value["name"], description = value["description"], aliases=value["aliases"])
        trinkets[key] = trinket

    return trinkets


def load_trinkets():
    if global_def.all_trinkets_loaded:
        return

    global_def.all_trinkets = load_trinkets_from_json(global_def.TRINKET_JSON_PATH)
    global_def.all_trinkets_loaded = True


def find_trinket_by_id(trinket_id: int) -> Trinket:
    load_trinkets()

    return global_def.all_trinkets.get(str(trinket_id), None)


def find_trinkets_by_name(search_string: str) -> list:
    load_trinkets()

    matched_trinkets = []
    for trinket in global_def.all_trinkets.values():
        if search_string in trinket.name and not trinket in matched_trinkets:
            matched_trinkets.append(trinket)

    for trinket in global_def.all_trinkets.values():
        for alias in trinket.aliases:
            if search_string in alias and not trinket in matched_trinkets:
                matched_trinkets.append(trinket)
    return matched_trinkets