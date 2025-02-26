from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment
import os
from pathlib import Path

from ..item_object import Item, load_items_from_json, find_item_by_id, find_items_by_name
from ..vague_search import create_image_with_list
from ..global_def import VAGUE_SEARCH_RES_PATH

isaac_item = on_command("item", aliases={"c"})

@isaac_item.handle()
async def handle_isaac_item(args: Message = CommandArg()):
    word = args.extract_plain_text().strip()
    similar_list = []

    if word.isdigit():
        num = int(word)
        similar_list.append(find_item_by_id(num))
    else:
        similar_list = find_items_by_name(word)

    if len(similar_list) == 0:
        await isaac_item.finish(Message("找不到对应的道具"))
        return
    
    if len(similar_list) == 1:
        item = similar_list[0]
        await isaac_item.finish(MessageSegment.image(Path(f'/root/bot/tools/item_des/item_des_{item.id}.png')))
        return

    create_image_with_list(similar_list)
    await isaac_item.finish(MessageSegment.image(Path(VAGUE_SEARCH_RES_PATH)))