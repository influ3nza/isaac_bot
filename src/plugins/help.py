from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from .. import group_management

send_help = on_command("help", aliases={"帮助"})

@send_help.handle()
async def handle_help(event: Event):
    if not group_management.accept_group_barrier(str(event.group_id)):
        return
    
    msg = "指令：-1|减1|减一|负1|负一|d-1\n参数：<id>/<道具名>\n作用：显示本道具5次D-1的结果\n\n"
    msg += "指令：+1|到|加一|加1\n参数：<id>/<道具名>\n作用：显示5次D-1可以达到本道具的结果\n\n"
    msg += "指令：item|c\n参数：<id>/<道具名>\n作用：搜索道具，支持字串模糊查找\n\n"
    msg += "指令：今天|早|中|晚饭|夜宵|下午茶吃什么\n参数：无\n作用：想不到吃什么的话，就交给以撒吧\n\n"
    msg += "指令：guess\n参数：<hint个数(可选，默认5)>\n作用：猜道具，在时间限制内使用/g <道具名>发送猜测。--目前功能较不完善，游戏体验可能较差--\n\n"
    msg += "指令：<正整数>(无需反斜杠)\n参数：无\n作用：发送贴吧谏言，目前只支持10。\n\n"
    msg += "指令：a<正整数>(无需反斜杠)\n参数：无\n作用：发送可爱的emoji，目前仅支持1。\n\n"
    msg += "\n目前道具绰号都基本加了一遍了，如果有少的跟我说，后续会开手动添加接口。"

    await send_help.finish(Message(msg))