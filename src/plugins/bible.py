from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from pathlib import Path
import random
from datetime import datetime

from .. import global_def
from .. import vague_search
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

    if len(word) == 0:
        return

    if word == "/bible":
        msg = Message()
        msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/emoji/bible.jpg"))
        await reply_bible.finish(msg)
        return
    
    if word == "/dr":
        msg = Message()
        msg += MessageSegment.image(Path(global_def.DR_PATH))
        msg += MessageSegment.text(datetime.now().strftime("%Y年%m月%d日\n"))
        msg += MessageSegment.text("今天的dr(版本为忏悔+)：\n")

        date = datetime.now().strftime("%m-%d")
        vague_search.dr_parse_image(int(date.split('-')[0]), int(date.split('-')[1]), global_def.DR_CROP_PATH)

        msg += MessageSegment.image(global_def.DR_TODAY_PATH)
        await reply_bible.finish(msg)
        return
    
    if word[0] != "a":
        word = word[1:]
        if word.isdigit():
            i_word = int(word)
            if i_word == 1:
                msg = Message()
                msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/other/emoji_{i_word}.png"))
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