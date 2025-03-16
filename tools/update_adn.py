import json

with open("./item.json", "r", encoding="utf-8") as file:
    items = json.load(file)

with open("adn_pending.json", "r", encoding="utf-8") as file:
    adns = json.load(file)

for key, value in adns.items():
    for v_item in items.values():
        if v_item["name"] != key:
            continue
        aliases = v_item["aliases"]
        print(aliases)
        for new_adn in value["adn"]:
            print(new_adn)
            if new_adn not in aliases:
                aliases.append(new_adn)

with open("./item.json", "w", encoding="utf-8") as file:
    json.dump(items, file, ensure_ascii=False, indent=2, separators=(",", ":"))

adns = {}

with open("adn_pending.json", "w", encoding="utf-8") as file:
    json.dump(adns, file, ensure_ascii=False, indent=2, separators=(",", ":"))