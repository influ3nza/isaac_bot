import json

from . import global_def

def load_replies_from_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    items = {}
    for key, value in json_data.items():
        items[key] = value
    return items

def load_replies():
    if global_def.all_replies_loaded:
        return
    
    global_def.all_replies = load_replies_from_json(global_def.REPLY_JSON_PATH)
    global_def.all_replies_loaded = True

def find_replies_by_label(label: str) -> list:
    load_replies()

    r_list = global_def.all_replies.get(label)
    return r_list