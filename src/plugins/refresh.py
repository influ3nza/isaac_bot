from nonebot import require, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot import on_command
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from .. import group_management
from ..secret import secrets
from .. import global_def

driver = get_driver()
on_refresh = on_command("refresh")

async def reset_global_dict():
    group_management.draw_card_record.clear()
    group_management.guess_record.clear()

@driver.on_startup
async def init_scheduler():
    scheduler.add_job(reset_global_dict,
    "cron",
    hour=4,
    minute=0,
    second=0,
    timezone="Asia/Shanghai")


@on_refresh.handle()
async def handle_refresh(bot: Bot, event: Event):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    if not str(event.user_id) in secrets.administrator:
        await handle_refresh.finish("你不是管理员，无法使用此功能！")
        return
    
    global_def.all_cards = {}
    global_def.all_cards_loaded = False
    global_def.all_items = {}
    global_def.all_items_loaded = False
    global_def.all_labels = {}
    global_def.all_labels_loaded = False
    global_def.all_replies = {}
    global_def.all_replies_loaded = False
    global_def.all_trinkets = {}
    global_def.all_trinkets_loaded = False

    await handle_refresh.finish("刷新成功！")