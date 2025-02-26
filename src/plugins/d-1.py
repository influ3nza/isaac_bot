from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

from ..item_object import Item, load_items_from_json, find_item_by_id, find_items_by_name
from ..vague_search import create_image_with_list
from ..adj_item import generate_image_sequence_down, create_concatenated_image
from ..global_def import VAGUE_SEARCH_RES_PATH, D_1_RES_PATH

D_1 = on_command("-1", aliases={"d-1", "减1", "负1", "减一", "负一"})

@D_1.handle()
async def handle_d_1(args: Message = CommandArg()):
    word = args.extract_plain_text().strip()
    similar_list = []

    if word.isdigit():
        num = int(word)
        similar_list.append(find_item_by_id(num))
    else:
        similar_list = find_items_by_name(word)

    if len(similar_list) == 0:
        await D_1.finish(Message("找不到对应的道具"))
        return
    
    if len(similar_list) == 1:
        item = similar_list[0]
        id_sequence = generate_image_sequence_down(item.id)

        create_concatenated_image(id_sequence, D_1_RES_PATH)
        await D_1.finish(MessageSegment.image(Path(D_1_RES_PATH)))
        return

    create_image_with_list(similar_list)
    await D_1.finish(MessageSegment.image(Path(VAGUE_SEARCH_RES_PATH)))