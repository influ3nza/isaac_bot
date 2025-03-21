all_items = {}
all_items_loaded = False
all_labels = {}
all_labels_loaded = False
all_replies = {}
all_replies_loaded = False
all_trinkets = {}
all_trinkets_loaded = False
all_cards = {}
all_cards_loaded = False

missing_item_number = {43, 61, 235, 587, 613, 620, 630, 648, 662, 666, 718, 298, 688, 674, 486}

ITEM_JSON_PATH = "/root/bot/isaac/tools/item.json"
TRINKET_JSON_PATH = "/root/bot/isaac/tools/trinket.json"
LABEL_JSON_PATH = "/root/bot/isaac/tools/label.json"
REPLY_JSON_PATH = "/root/bot/isaac/tools/reply.json"
CARD_JSON_PATH = "/root/bot/isaac/tools/card.json"

FONT_PATH = "/root/bot/isaac/tools/yahei.ttf"
VAGUE_SEARCH_RES_PATH_PREFIX = "/root/bot/out/vague_res_"
D_1_RES_PATH = "/root/bot/out/d_1_res.png"
D_p1_RES_PATH = "/root/bot/out/d_p1_res.png"
SPRITE_GUESS_PATH = "/root/bot/out/sprite_guess.png"
TMT_RES_PATH_PREFIX = "/root/bot/out/tmt_res_"
DR_TODAY_PATH = "/root/bot/out/dr_today.png"

DICE_FETCH_PATH = "/root/bot/isaac/tools/dice/"
ITEM_SPRITE_PATH_PREFIX = "/root/bot/isaac/tools/item_sprite/item_sprite_"
ITEM_DES_PATH_PREFIX = "/root/bot/isaac/tools/item_des/item_des_"
TRINKET_SPRITE_PATH_PREFIX = "/root/bot/isaac/tools/trinket_sprite/trinket_sprite_"
TRINKET_DES_PATH_PREIFX = "/root/bot/isaac/tools/trinket_des/trinket_des_"
CARD_SPRITE_PATH_PREFIX = "/root/bot/isaac/tools/card_sprite/card_sprite_"
ITEM_EFFECT_PATH = "/root/bot/isaac/tools/pickup_effect/"

# files that need to write frequently
ADN_PENDING_PATH = "/root/bot/isaac/tools/adn_pending.json"
GAME_RECORDS_PATH = "/root/bot/isaac/tools/game_records.json"

PNG_SUFFIX = ".png"

UNDER_CONSTRUCTION_HINT_PATH = "/root/bot/isaac/tools/item_sprite/item_sprite_481.png"
BIBLE_PATH = "/root/bot/isaac/tools/other/bible.jpg"
DR_PATH = "/root/bot/isaac/tools/other/dr2025.jpeg"
DR_CROP_PATH = "/root/bot/isaac/tools/other/dr2025_crop.jpeg"

bible_reply_prefix = "bible_"
who_asked_prefix = "who_asked_"
debug3_prefix = "debug3_"
rewind_prefix = "rewind_"
prophesy_prefix = "prophesy_"