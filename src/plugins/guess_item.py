from nonebot import on_command
from nonebot import on_message
from nonebot.params import CommandArg
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
import os
from pathlib import Path
import random
import asyncio

from ..item_object import Item, load_items_from_json, find_item_by_id, find_items_by_name_strict, find_items_by_name
from .. import global_def
from ..label_object import Label, load_labels

guess_item = on_command("guess")
make_guess = on_message()
game_start = -1
timeout_task = None
label_list = []
hints = 5

async def game_timeout(bot: Bot, group_id: int):
    global label_list, game_start, hints

    # 组装label列表
    try:
        load_labels()

        item = find_item_by_id(game_start)
        for label_id in item.labels_id:
            label = global_def.all_labels.get(str(label_id))
            if label:
                label_list.append(label)

        # 品质
        label_list.append(Label(1000, "道具品质", f"这个道具的品质是{item.rarity}级。"))

        # 主动被动
        if item.charge != str(-1):
            label_list.append(Label(1001, "主动被动", f"这个道具是主动道具，且充能为{item.charge}。"))
        else:
            label_list.append(Label(1001, "主动被动", f"这个道具是被动道具。"))

        #名字
        label_list.append(Label(1002, "道具名", f"这个道具的名字一共有{len(item.name)}个字符(汉字、字母、符号)。"))

        #描述
        des = item.description
        rand_len = random.randint(2, 3)
        if (len(des) < 3):
            rand_len = len(des)

        rand_start = random.randint(0, len(des)-rand_len)
        label_list.append(Label(1003, "附加描述", f"这个道具的附加描述的一部分为\"{des[rand_start : rand_start+rand_len]}\"。"))

        sent_list = []
        msg = Message()

        # 提示个数
        hints = min(hints, len(label_list))
        msg += MessageSegment.text(f"本轮游戏共有{hints}个提示。\n\n")

        now_send = random.randint(0, len(label_list)-1)
        while label_list[now_send].id in sent_list:
            now_send = random.randint(0, len(label_list)-1)
        
        sent_list.append(label_list[now_send].id)
        msg += MessageSegment.text("1." + label_list[now_send].description + "\n\n")
        await bot.send_msg(group_id=group_id, message=msg)
        await asyncio.sleep(10)

        send_cnt = hints - 1
        if send_cnt > len(label_list)-1:
            send_cnt = len(label_list)-1

        for i in range(send_cnt):
            now_send = random.randint(0, len(label_list)-1)
            while label_list[now_send].id in sent_list:
                now_send = random.randint(0, len(label_list)-1)
            
            sent_list.append(label_list[now_send].id)
            msg += MessageSegment.text(str(i+2) + "." + label_list[now_send].description + "\n\n")
            await bot.send_msg(group_id=group_id, message=msg)
            await asyncio.sleep(20)

        if game_start != -1:
            temp_id = game_start
            game_start = -1
            end_msg = Message()
            end_msg += MessageSegment.text("时间到！游戏结束！正确答案是")
            end_msg += MessageSegment.image(Path(f"/root/bot/tools/item_sprite/item_sprite_{temp_id}.png"))
            end_msg += MessageSegment.text(find_item_by_id(temp_id).name)
            label_list.clear()
            hints = 5
            await bot.send_msg(group_id=group_id, message=end_msg)

    except Exception as e:
        await bot.send_msg(group_id=group_id, message=f"游戏出错：{str(e)}")
        label_list.clear()
        game_start = -1

@guess_item.handle()
async def handle_guess_item(bot: Bot, event: Event):
    global game_start, timeout_task, hints
    if game_start != -1:
        msg = Message("此轮游戏还未结束！")
        await guess_item.finish(msg)
        return
    
    load_labels()

    game_start = random.randint(1, 732)
    while (game_start in global_def.missing_item_number):
        game_start = random.randint(1, 732)

    word = event.get_message().extract_plain_text().strip()
    if word.isdigit() and int(word) > 5:
        hints = int(word)

    group_id = event.group_id
    timeout_task = asyncio.create_task(game_timeout(bot, group_id))
    await guess_item.finish(Message(f"以撒点子王！每隔一段时间就会放出该物品的一个提示。如果道具名长度大于2，除非回答准确绰号，否则只匹配至少长度为3的子串。\n发送quit停止。"))


@make_guess.handle()
async def handle_make_guess(event: Event):
    global game_start
    if game_start == -1:
        return

    word = event.get_message().extract_plain_text().strip()
    if len(word) == 0:
        return
    
    if word.isdigit():
        if int(word) == game_start:
            msg = Message()
            msg += MessageSegment.text("猜测正确！正确答案是")
            msg += MessageSegment.image(Path(f"/root/bot/tools/item_sprite/item_sprite_{game_start}.png"))
            msg += MessageSegment.text(find_item_by_id(game_start).name)
            label_list.clear()
            hints = 5
            game_start = -1
            if timeout_task:
                timeout_task.cancel()
            await make_guess.finish(msg)
            return

    if game_start in [item.id for item in find_items_by_name(word)]:
        msg = Message()
        msg += MessageSegment.text("猜测正确！正确答案是")
        msg += MessageSegment.image(Path(f"/root/bot/tools/item_sprite/item_sprite_{game_start}.png"))
        msg += MessageSegment.text(find_item_by_id(game_start).name)
        label_list.clear()
        hints = 5
        game_start = -1
        if timeout_task:
            timeout_task.cancel()
        await make_guess.finish(msg)
        return

    elif word == "quit":
        msg = Message()
        msg += MessageSegment.text("结束，正确答案是")
        msg += MessageSegment.image(Path(f"/root/bot/tools/item_sprite/item_sprite_{game_start}.png"))
        msg += MessageSegment.text(find_item_by_id(game_start).name)
        label_list.clear()
        hints = 5
        game_start = -1
        if timeout_task:
            timeout_task.cancel()
        await make_guess.finish(msg)
        return
