from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import os
from pathlib import Path

from ..item_object import Item
from .. import item_object
from .. import vague_search
from .. import global_def
from .. import group_management
from .. import adn_utils

add_adn = on_command("addadn", aliases={"addnickname", "添加昵称", "addalias"})
show_adn = on_command("adn", aliases={"nickname", "alias", "昵称"})

@show_adn.handle()
async def show_adn_handle(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    similar_list = []
    
    word = args.extract_plain_text().strip()
    if len(word) == 0:
        return
    
    elif word.isdigit():
        num = int(word)
        similar_list.append(item_object.find_item_by_id(num))
    else:
        similar_list = item_object.find_items_by_name(word)

    if len(similar_list) == 0:
        await show_adn.finish(Message("找不到对应的道具"))
        return
    
    if len(similar_list) == 1:
        item = similar_list[0]
        msg = Message()
        msg += MessageSegment.image(Path(global_def.ITEM_SPRITE_PATH_PREFIX + str(item.id) + global_def.PNG_SUFFIX))
        msg += MessageSegment.text(item.name + "有以下昵称：\n")
        for alias in item.aliases:
            msg += MessageSegment.text("-  " + alias + "\n")
        await show_adn.finish(msg)
        return

    vague_search.create_image_with_list(similar_list, "ITEM", group_id)
    await show_adn.finish(MessageSegment.image(Path(global_def.VAGUE_SEARCH_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX)))


@add_adn.handle()
async def add_adn_handle(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    similar_list = []
    
    word = args.extract_plain_text().strip()
    if len(word) == 0:
        return
    
    arg_list = word.split(' ')
    if len(arg_list) != 2:
        add_adn.finish("发送/help查看正确语法。")
        return
    
    item_word = arg_list[0]
    new_adn = arg_list[1]

    if item_word.isdigit():
        num = int(item_word)
        similar_list.append(item_object.find_item_by_id(num))
    else:
        similar_list = item_object.find_items_by_name(item_word)

    if len(similar_list) == 0:
        await add_adn.finish(Message("找不到对应的道具"))
        return
    
    if len(similar_list) == 1:
        item = similar_list[0]
        adn_utils.add_pending_adn(item.name, new_adn)
        await add_adn.finish("已添加进waiting list，记得戳电容让他更新。")
        return

    vague_search.create_image_with_list(similar_list, "ITEM", group_id)
    await add_adn.finish(MessageSegment.image(Path(global_def.VAGUE_SEARCH_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX)))
