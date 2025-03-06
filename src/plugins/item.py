from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import os
from pathlib import Path

from ..item_object import Item, Trinket
from .. import item_object
from .. import vague_search
from .. import global_def
from .. import group_management

isaac_item = on_command("item", aliases={"c"})
isaac_trinket = on_command("trinket", aliases={"t"})

@isaac_item.handle()
async def handle_isaac_item(event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    word = args.extract_plain_text().strip()
    similar_list = []

    if len(word) == 0:
        return
    elif word.isdigit():
        num = int(word)
        similar_list.append(item_object.find_item_by_id(num))
    else:
        similar_list = item_object.find_items_by_name(word)

    if len(similar_list) == 0:
        await isaac_item.finish(Message("找不到对应的道具"))
        return
    
    if len(similar_list) == 1:
        item = similar_list[0]
        await isaac_item.finish(MessageSegment.image(Path(global_def.ITEM_DES_PATH_PREFIX + str(item.id) + global_def.PNG_SUFFIX)))
        return

    vague_search.create_image_with_list(similar_list, "ITEM", group_id)
    await isaac_item.finish(MessageSegment.image(Path(global_def.VAGUE_SEARCH_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX)))


@isaac_trinket.handle()
async def handle_isaac_trinket(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    word = args.extract_plain_text().strip()
    similar_list = []

    if len(word) == 0:
        return
    elif word.isdigit():
        num = int(word)
        similar_list.append(item_object.find_trinket_by_id(num))
    else:
        similar_list = item_object.find_trinkets_by_name(word)

    if len(similar_list) == 0:
        await isaac_trinket.finish(Message("找不到对应的饰品"))
        return
    
    if len(similar_list) == 1:
        trinket = similar_list[0]
        await isaac_trinket.finish(MessageSegment.image(Path(global_def.TRINKET_DES_PATH_PREIFX + str(trinket.id) + global_def.PNG_SUFFIX)))
        return

    vague_search.create_image_with_list(similar_list, "TRINKET", group_id)
    await isaac_trinket.finish(MessageSegment.image(Path(global_def.VAGUE_SEARCH_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX)))