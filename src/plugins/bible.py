from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from pathlib import Path
import random

from .. import global_def
from .. import category_sets
from .. import group_management
from .. import reply_object

# 定义一个消息处理器
reply_bible = on_message()

@reply_bible.handle()
async def handle_bible(bot: Bot, event: Event):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    if event.user_id == event.self_id:
        return
    
    word = event.get_message().extract_plain_text().strip()

    if word == "/bible":
        msg = Message()
        msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/emoji/bible.jpg"))
        await reply_bible.finish(msg)
        return

    if word.isdigit() or word == "-1":
        s_key = global_def.bible_reply_prefix + word
        r_list = reply_object.find_replies_by_label(s_key)

        if r_list:
            await reply_bible.finish(Message(r_list[random.randint(0, len(r_list)-1)]))
        return
    
    if word.startswith("你怎么知道") and len(word) > 10:
        reply = ""
        for i in range(1, 4):
            s_key = global_def.who_asked_prefix + str(i)
            r_list = reply_object.find_replies_by_label(s_key)
            reply += r_list[random.randint(0, len(r_list)-1)]

        await reply_bible.finish(Message(reply))
        return
    
    if word.count("既然") == 1 and word.count("不如") == 1:
        if word.find("既然") < word.find("不如"):
            s_key = global_def.debug3_prefix
            r_list = reply_object.find_replies_by_label(s_key)

            await reply_bible.finish(Message(r_list[random.randint(0, len(r_list)-1)]))
            return
        
    if word.startswith("rewind"):
        s_key = global_def.rewind_prefix
        r_list = reply_object.find_replies_by_label(s_key)

        await reply_bible.finish(Message(r_list[random.randint(0, len(r_list)-1)]))
        return