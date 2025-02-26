import json

from .global_def import all_items, all_items_loaded
from .global_def import ITEM_JSON_PATH

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
    global all_items, all_items_loaded
    if all_items_loaded == True:
        return

    all_items = load_items_from_json(ITEM_JSON_PATH)
    all_items_loaded = True

def find_item_by_id(item_id: int) -> Item:
    global all_items
    load_items()

    return all_items.get(str(item_id), None)

def find_items_by_name(search_string: str) -> list:
    global all_items
    load_items()

    matched_items = []
    for item in all_items.values():
        if search_string in item.name and not item in matched_items:
            matched_items.append(item)

    for item in all_items.values():
        for alias in item.aliases:
            if search_string in alias and not item in matched_items:
                matched_items.append(item)
    return matched_items

def find_items_by_name_strict(search_string: str) -> list:
    global all_items
    load_items()

    matched_items = []
    for item in all_items.values():
        if len(item.name) > 2:
            if len(search_string) > 2 and search_string in item.name and not item in matched_items:
                matched_items.append(item)
        else:
            if search_string in item.name and not item in matched_items:
                matched_items.append(item)
    
    for item in all_items.values():
        if search_string in item.aliases and not item in matched_items:
            matched_items.append(item)
    return matched_items