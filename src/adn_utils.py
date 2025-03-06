from . import global_def
import json

def add_pending_adn(item_name: str, new_adn: str):
    with open(global_def.ADN_PENDING_PATH, "r", encoding="utf-8") as file:
        adn_pendings = json.load(file)

    if item_name not in adn_pendings:
        adn_pendings[item_name] = {"adn": []}

    if "adn" not in adn_pendings[item_name] or not isinstance(adn_pendings[item_name]["adn"], list):
        adn_pendings[item_name]["adn"] = []

    if new_adn not in adn_pendings[item_name]["adn"]:
        adn_pendings[item_name]["adn"].append(new_adn)

    with open(global_def.ADN_PENDING_PATH, 'w') as file:
        json.dump(adn_pendings, file, indent=4, ensure_ascii=False)