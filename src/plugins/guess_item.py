from nonebot import on_command
from nonebot import on_message
from nonebot import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from pathlib import Path
import random
import asyncio

from .. import item_object
from .. import label_object
from .. import global_def
from .. import group_management
from .. import adj_item
from .. import file_utils

from ..label_object import Label

guess_item = on_command("guess", aliases={"g", "猜", "猜道具"})
guess_sprite = on_command("gs", aliases={"猜图片"})
make_guess = on_message()

def clear_game_status(group_id: str) -> dict:
    if group_management.group_guess_game.get(group_id) != None and group_management.group_guess_game[group_id]["timeout_task"]:
        group_management.group_guess_game[group_id]["timeout_task"].cancel()

    group_management.group_guess_game[group_id] = {
        "game_start": -1,
        "type": -1,
        "hints": 6,
        "label_list": [],
        "timeout_task": None,
        "guess_chance": {}
    }

    return group_management.group_guess_game[group_id]


async def guess_game_timeout(bot: Bot, group_id: str):
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    status = group_management.group_guess_game.get(str(group_id))
    if status == None:
        await bot.send_msg(group_id=group_id, message="不存在该群组的游戏记录，请联系管理员。")
        return
    
    logger.info("status: " + str(status))
    
    game_start = status["game_start"]
    label_list = []
    hints = status["hints"]

    # 组装label列表
    try:
        item = item_object.find_item_by_id(game_start)
        for label_id in item.labels_id:
            label = label_object.find_label_by_id(str(label_id))
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
        rand_len = random.randint(1, 2)
        if (len(des) < 2):
            rand_len = len(des)
        rand_start = random.randint(0, len(des)-rand_len)
        label_list.append(Label(1003, "附加描述", f"这个道具的附加描述的一部分为\"{des[rand_start : rand_start+rand_len]}\"。"))
        logger.info(label_list)

        sent_list = []
        msg = Message()

        # 提示个数
        hints = min(hints, len(label_list))
        msg += MessageSegment.text(f"本轮游戏共有{hints}个提示。\n\n")

        now_send = random.randint(0, len(label_list)-1)
        while label_list[now_send].id in sent_list:
            now_send = random.randint(0, len(label_list)-1)
        
        sent_list.append(label_list[now_send].id)
        msg += MessageSegment.text("1." + label_list[now_send].description + "\n")
        await bot.send_msg(group_id=group_id, message=msg)
        await asyncio.sleep(5)

        send_cnt = hints - 1
        if send_cnt > len(label_list)-1:
            send_cnt = len(label_list)-1

        for i in range(send_cnt):
            now_send = random.randint(0, len(label_list)-1)
            while label_list[now_send].id in sent_list:
                now_send = random.randint(0, len(label_list)-1)
            
            sent_list.append(label_list[now_send].id)
            msg += MessageSegment.text("\n" + str(i+2) + "." + label_list[now_send].description + "\n")
            
            await bot.send_msg(group_id=group_id, message=msg)
            if i == send_cnt-1:
                await asyncio.sleep(25)
            else:
                await asyncio.sleep(15)

        if status["game_start"] != -1:
            end_msg = Message()
            end_msg += MessageSegment.text("时间到！游戏结束！正确答案是")
            end_msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/item_sprite/item_sprite_{status['game_start']}.png"))
            end_msg += MessageSegment.text(item_object.find_item_by_id(status["game_start"]).name)

            clear_game_status(str(group_id))
            await bot.send_msg(group_id=group_id, message=end_msg)

    except Exception as e:
        clear_game_status(str(group_id))
        await bot.send_msg(group_id=group_id, message=f"游戏出错：{str(e)}")


async def sprite_game_timeout(bot: Bot, group_id: str):
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    status = group_management.group_guess_game.get(str(group_id))
    if status == None:
        await bot.send_msg(group_id=group_id, message="不存在该群组的游戏记录，请联系管理员。")
        return
    
    game_start = status["game_start"]
    adj_item.create_blurred_sprite(game_start)
    msg = Message()
    msg += MessageSegment.text("这是什么道具？")
    msg += MessageSegment.image(Path(global_def.SPRITE_GUESS_PATH))
    await bot.send_msg(group_id=group_id, message=msg)

    await asyncio.sleep(25)

    status = group_management.group_guess_game.get(str(group_id))
    game_start = status["game_start"]
    if game_start != -1:
        end_msg = Message()
        end_msg += MessageSegment.text("时间到！游戏结束！正确答案是")
        end_msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/item_sprite/item_sprite_{game_start}.png"))
        end_msg += MessageSegment.text(item_object.find_item_by_id(game_start).name)

        clear_game_status(str(group_id))
        await bot.send_msg(group_id=group_id, message=end_msg)


@guess_item.handle()
async def handle_guess_item(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    # if not group_management.test_barrier(str(group_id)):
    #     msg = Message()
    #     msg += MessageSegment.text("还在g还在g。")
    #     msg += MessageSegment.image(Path(global_def.UNDER_CONSTRUCTION_HINT_PATH))
    #     await bot.send_msg(group_id=group_id, message=msg)
    #     return

    status = group_management.group_guess_game.get(str(group_id))
    if status == None:
        status = clear_game_status(str(group_id))

    if status["game_start"] != -1:
        await guess_item.finish(Message("此轮游戏还未结束！"))
        return
    
    # 控制游戏次数 < 6
    game_record = group_management.guess_record.get(str(event.user_id))
    if game_record == None:
        group_management.guess_record[str(event.user_id)] = 1
    else:
        if game_record >= 6:
            await guess_item.finish("你已经猜太多次了，等明天再来吧！")
            return
        group_management.guess_record[str(event.user_id)] += 1
        logger.info(f"play count: {group_management.guess_record[str(event.user_id)]}")

    status = clear_game_status(str(group_id))

    game_start = random.randint(1, 732)
    while (game_start in global_def.missing_item_number):
        game_start = random.randint(1, 732)
    status["game_start"] = game_start
    status["type"] = 1

    word = args.extract_plain_text().strip()
    if word.isdigit() and int(word) > 0:
        status["hints"] = int(word)

    status["timeout_task"] = asyncio.create_task(guess_game_timeout(bot, group_id))

    status = group_management.group_guess_game.get(str(group_id))
    await guess_item.finish(Message(f"以撒点子王！每隔一段时间就会放出该物品的一个提示。如果道具名长度大于2，除非回答准确绰号，否则只匹配至少长度为3的子串。\n需要在回答前加上\'g\'。\n不能回答\"妈妈的\"、\"嗝屁猫\"这三个字!!!\n支持英语大小写识别。\n每轮游戏每人最多猜测3次。\n发送quit停止。"))


@guess_sprite.handle()
async def handle_guess_sprite(bot: Bot, event: Event):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return

    status = group_management.group_guess_game.get(str(group_id))
    if status == None:
        status = clear_game_status(str(group_id))

    if status["game_start"] != -1:
        await guess_sprite.finish(Message("此轮游戏还未结束！"))
        return
    
    # if not group_management.test_barrier(str(group_id)):
    #     msg = Message()
    #     msg += MessageSegment.text("还在修。")
    #     msg += MessageSegment.image(Path(global_def.UNDER_CONSTRUCTION_HINT_PATH))
    #     await bot.send_msg(group_id=group_id, message=msg)
    #     return

    status = clear_game_status(str(group_id))

    game_start = random.randint(1, 732)
    while (game_start in global_def.missing_item_number):
        game_start = random.randint(1, 732)
    status["game_start"] = game_start
    status["type"] = 2

    status["timeout_task"] = asyncio.create_task(sprite_game_timeout(bot, group_id))
    await guess_sprite.finish(Message(f"根据道具图片猜测是什么道具。图片可能被横置或倒转。\n发送quit停止。"))


@make_guess.handle()
async def handle_make_guess(bot: Bot, event: Event):
    group_id = event.group_id
    if not group_management.accept_group_barrier(str(group_id)):
        return
    
    if event.user_id == event.self_id:
        return
    
    status = group_management.group_guess_game.get(str(group_id))
    if status == None:
        return
    
    game_start = status["game_start"]
    if game_start == -1:
        return
    
    # if not group_management.test_barrier(str(group_id)):
    #     msg = Message()
    #     msg += MessageSegment.text("还在修。")
    #     msg += MessageSegment.image(Path(global_def.UNDER_CONSTRUCTION_HINT_PATH))
    #     await bot.send_msg(group_id=group_id, message=msg)
    #     return
    
    # 摘取猜测的词语
    word = event.get_message().extract_plain_text().strip()
    if len(word) == 0:
        return
    
    if word == "妈妈的" or word == "g妈妈的":
        await make_guess.finish("你妈的")
        return
    
    if word == "嗝屁猫" or word == "g嗝屁猫":
        await make_guess.finish("哈基米")
        return
    
    if word != "quit":
        if word[0] != 'g':
            return
        else:
            word = word[1:]
    
    msg = Message()
    need_add_score = False

    # 判断是否猜测超过一定数目
    if word != "quit" and len(word) <= 6 and status["type"] == 1:
        if str(event.user_id) not in status["guess_chance"]:
            status["guess_chance"][str(event.user_id)] = 1
        else:
            if status["guess_chance"][str(event.user_id)] >= 3:
                stop_msg = Message()
                stop_msg += MessageSegment.at(event.user_id)
                stop_msg += MessageSegment.text("猜测次数过多，请等下一轮游戏！")
                await make_guess.finish(stop_msg)
                return
            else:
                status["guess_chance"][str(event.user_id)] += 1

    # 猜测结果判断
    if word.isdigit() and int(word) == game_start:
        msg += MessageSegment.at(event.user_id)
        msg += MessageSegment.text("\n猜测正确！正确答案是")
        need_add_score = True

    elif game_start in [item.id for item in item_object.find_items_by_name_strict(word)]:
        msg += MessageSegment.at(event.user_id)
        msg += MessageSegment.text("\n猜测正确！正确答案是")
        need_add_score = True

    elif word == "quit":
        msg += MessageSegment.text("结束，正确答案是")
    
    else:
        return

    # 猜测结果发送
    msg += MessageSegment.image(Path(f"/root/bot/isaac/tools/item_sprite/item_sprite_{game_start}.png"))
    msg += MessageSegment.text(item_object.find_item_by_id(game_start).name)

    if need_add_score:
        msg += MessageSegment.text(f"\nTA已经猜对{file_utils.guess_add_score(str(event.user_id))}次了！")
    
    if status["timeout_task"]:
        status["timeout_task"].cancel()
    
    clear_game_status(str(group_id))
    await make_guess.finish(msg)
    return
