from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from pathlib import Path
import random

from .. import group_management
from .. import global_def

roll_dice = on_message()

@roll_dice.handle()
async def handle_roll_dice(bot: Bot, event: Event):
    if not group_management.accept_group_barrier(str(event.group_id)):
        return
    
    word = event.get_message().extract_plain_text().strip()

    if word == "1d6":
        res = random.randint(1, 6)
        msg = Message()
        msg += MessageSegment.image(Path(global_def.DICE_FETCH_PATH + f"d6_{res}.png"))
        await roll_dice.finish(msg)
        return
    
    if word == "1d20":
        res = random.randint(1, 20)
        msg = Message()
        msg += MessageSegment.image(Path(global_def.DICE_FETCH_PATH + f"d20_{res}.png"))
        await roll_dice.finish(msg)
        return