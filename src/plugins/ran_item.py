from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import random
from pathlib import Path

from ..global_def import missing_item_number
from ..category_sets import isaac_flavor_text
from ..item_object import find_item_by_id
from .. import group_management

rand_item = on_command("今天吃什么", aliases={"早饭吃什么", "午饭吃什么", "晚饭吃什么", "下午茶吃什么", "夜宵吃什么", "早上吃什么", "中午吃什么", "晚上吃什么", "下午吃什么"})

@rand_item.handle()
async def handle_rand_item(event: Event):
    if not group_management.accept_group_barrier(str(event.group_id)):
        return
    
    rand = random.randint(1, 732)
    while (rand in missing_item_number):
        rand = random.randint(1, 732)

    item = find_item_by_id(rand)

    msg = Message()
    if rand != 721:
        msg += MessageSegment.text("来吃")
    msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/item_sprite/item_sprite_{rand}.png"))
    if rand != 721:
        msg += MessageSegment.text(f"{item.name}吧！")

    for set_name, set_info in isaac_flavor_text.items():
        if rand in set_info["id"]:
            msg += MessageSegment.text(set_info["text"])

    await rand_item.finish(msg)