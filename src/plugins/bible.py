from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from pathlib import Path
import random

from ..global_def import accept_group_id
from ..category_sets import who_asked, sequence_word, r_please

# 定义一个消息处理器
reply_bible = on_message()

@reply_bible.handle()
async def handle_bible(bot: Bot, event: Event):
    group_id = event.group_id
    if str(group_id) not in accept_group_id:
        return
    
    word = event.get_message().extract_plain_text().strip()
    if word == "10":
        await reply_bible.finish(Message("r了吧，这把算你赢了。"))
        return
    
    if word == "/bible":
        msg = Message()
        msg += MessageSegment.image(Path(f"/root/bot/tools/emoji/bible.jpg"))
        await reply_bible.finish(msg)
        return
    
    if word.startswith("你怎么知道") and len(word) > 10:
        global who_asked, sequence_word, r_please
        msg = Message()
        msg += MessageSegment.text(who_asked[random.randint(0, len(who_asked)-1)] + sequence_word[random.randint(0, len(sequence_word)-1)] + r_please[random.randint(0, len(r_please)-1)])
        await reply_bible.finish(msg)
        return