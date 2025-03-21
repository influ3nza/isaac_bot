from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from pathlib import Path
import random

from .. import global_def
from .. import group_management
from .. import card_object
from .. import deepseek

from ..card_object import Card

# 定义一个消息处理器
reply_card = on_command("lotd", aliases={"抽卡", "draw", "jrys", "今日运势"})


def rand_special() -> Card:
    length = len(card_object.special_drawables)
    rand_id = card_object.special_drawables[random.randint(0, length-1)]

    return card_object.find_card_by_id(rand_id)


def rand_normal() -> Card:
    length = len(card_object.normal_cards)
    rand_id = card_object.normal_cards[random.randint(0, length-1)]

    return card_object.find_card_by_id(rand_id)


@reply_card.handle()
async def handle_card(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    if event.user_id == event.self_id:
        return
    
    # if not group_management.test_barrier(str(group_id)):
    #     msg = Message()
    #     msg += MessageSegment.text("还在修。")
    #     msg += MessageSegment.image(Path(global_def.UNDER_CONSTRUCTION_HINT_PATH))
    #     await bot.send_msg(group_id=group_id, message=msg)
    #     return
    
    word = args.extract_plain_text().strip()
    
    cnt = group_management.draw_card_record.get(str(event.user_id))
    if cnt:
        if cnt == 2:
            await reply_card.finish("抽卡盒已经空了，要不明天再来？")
            return
        group_management.draw_card_record[str(event.user_id)] += 1
    else:
        group_management.draw_card_record[str(event.user_id)] = 1

    check = random.randint(1, 20)
    if check == 1:
        card = rand_special()
    else:
        card = rand_normal()

    msg = Message()
    msg += MessageSegment.at(event.user_id)
    msg += MessageSegment.text("\n正在解读牌意......")
    await bot.send_msg(group_id=group_id, message=msg)

    msg = Message()
    msg += MessageSegment.at(event.user_id)
    msg += MessageSegment.text("\nLuck of the draw!\n")
    msg += MessageSegment.image(Path(global_def.CARD_SPRITE_PATH_PREFIX + str(card.id) + global_def.PNG_SUFFIX))
    msg += MessageSegment.text(card.name + " <<" + card.description + ">>\n")

    wcnt = random.randint(10, 32)
    prompt = f"把塔罗牌：[{card.name}]的主要寓意总结为若干个关键词。以其中的随机一个关键词为主题写一段文字（如果方括号中包含问号，则代表对应卡牌的逆位卡牌，需包含消极旨意）。回答中不能出现卡牌名、逆位、关键词、寓意等任何无关的信息。回答需对仗、押韵、文学性强、不得加粗。回答只能包括那段文字，且不超过{wcnt}字。"
    response = await deepseek.amake_chat(prompt) 
    msg += MessageSegment.text(response)

    await reply_card.finish(msg)