from nonebot import require, get_driver
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from .. import group_management

driver = get_driver()

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