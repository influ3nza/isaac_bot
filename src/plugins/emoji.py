from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from pathlib import Path

from ..global_def import accept_group_id
from .. import group_management

# 定义一个消息处理器
reply_emoji = on_message()

@reply_emoji.handle()
async def handle_emoji(bot: Bot, event: Event):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    word = event.get_message().extract_plain_text().strip()
    if len(word) > 0 and word[0] != "a":
        return
    
    word = word[1:]
    if word.isdigit():
        i_word = int(word)
        if i_word == 1:
            msg = Message()
            msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/emoji/emoji_{i_word}.png"))
            await reply_emoji.finish(msg)