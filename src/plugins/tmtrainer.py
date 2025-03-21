from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from pathlib import Path

from .. import group_management, global_def, vague_search

tmt_gen = on_command("tmtrainer", aliases={"TMT", "TMTrainer", "tmt", "错误技"})

@tmt_gen.handle()
async def handle_tmt_gen(bot: Bot, event: Event):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    vague_search.create_error_item_image(group_id)

    msg = Message()
    msg += MessageSegment.image(Path(global_def.TMT_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX))

    await tmt_gen.finish(msg)