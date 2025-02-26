from nonebot import logger
import json

from . import global_def
from .global_def import LABEL_JSON_PATH

class Label:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


def load_label_from_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    labels = {}
    for key, value in json_data.items():
        if value.get("weight") == 0:
            continue
        
        label = Label(id=value["label_id"], name=value["label_name"], description = value["description"])
        labels[str(key)] = label

    return labels

def load_labels():
    if global_def.all_labels_loaded:
        return

    global_def.all_labels = load_label_from_json(LABEL_JSON_PATH)
    global_def.all_labels_loaded = True