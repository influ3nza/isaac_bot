from nonebot import on_notice
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, NoticeEvent, Message, MessageSegment
import random
from pathlib import Path

from .. import group_management
from .. import global_def
from .. import reply_object

send_prophesy = on_notice()

@send_prophesy.handle()
async def handle_send_prophesy(bot: Bot, event: NoticeEvent):
    if not group_management.accept_group_barrier(str(event.group_id)):
        return
    
    # if not group_management.test_barrier(str(event.group_id)):
    #     msg = Message()
    #     msg += MessageSegment.text("还在修。")
    #     msg += MessageSegment.image(Path(global_def.UNDER_CONSTRUCTION_HINT_PATH))
    #     await bot.send_msg(group_id=event.group_id, message=msg)
    #     return
    
    if not event.target_id == event.self_id:
        return
    
    s_key = global_def.prophesy_prefix
    r_list = reply_object.find_replies_by_label(s_key)

    if r_list:
        await send_prophesy.finish(Message(r_list[random.randint(0, len(r_list)-1)]))
    return