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

    
def guess_add_score(usr_id: str) -> int:
    with open(global_def.GAME_RECORDS_PATH, "r", encoding="utf-8") as file:
        game_records = json.load(file)
    
    if usr_id not in game_records:
        game_records[usr_id] = 1

    else:
        game_records[usr_id] += 1

    with open(global_def.GAME_RECORDS_PATH, 'w') as file:
        json.dump(game_records, file, indent=4, ensure_ascii=False)

    return game_records[usr_id]