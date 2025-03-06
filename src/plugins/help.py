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
    msg += "指令：item|c\n参数：<id>/<道具名>\n作用：搜索道具，支持字串、昵称模糊查找\n\n"
    msg += "指令：trinket|t\n参数：<id>/<饰品名>\n作用：搜索道具，支持字串、昵称模糊查找 --目前金饰品、妈盒效果还不完善，请协助--\n\n"
    msg += "指令：今天|早|中|晚饭|夜宵|下午茶吃什么\n参数：无\n作用：想不到吃什么的话，就交给以撒吧\n\n"
    msg += "指令：g\n参数：<hint个数(可选，默认7)>\n作用：猜道具，在时间限制内直接发送道具名、昵称或道具id进行猜测 --目前功能较不完善，游戏体验可能较差--\n\n"
    msg += "指令：gs\n参数：无\n作用：通过图片猜道具，在时间限制内直接发送道具名、昵称或道具id进行猜测 --目前功能较不完善，游戏体验可能较差--\n\n"
    msg += "指令：<正整数>(无需反斜杠)\n参数：无\n作用：发送贴吧谏言。使用/bible查看所有贴吧谏言\n\n"
    msg += "指令：a<正整数>(无需反斜杠)\n参数：无\n作用：发送可爱的emoji，目前仅支持1\n\n"
    msg += "指令：1d6|1d20(无需反斜杠)\n参数：无\n作用：转动命运之轮\n\n"
    msg += "戳一戳：揭示一条预言\n\n"
    msg += "指令：adn|nickname|alias|昵称\n参数：<id>/<道具名>\n作用：显示道具昵称\n\n"
    msg += "指令：addadn|addnickname|addalias|添加昵称\n参数：<id>/<道具名> <昵称名>\n作用：添加道具昵称，不会立即更新\n\n"
    msg += "???犹大似乎还有什么秘密......(此功能还没做好)"

    await send_help.finish(Message(msg))