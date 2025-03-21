from PIL import Image, ImageDraw, ImageFont
from nonebot import logger
import os
import random

from . import global_def

def create_image_with_list(object_list, type, group_id):
    font_size = 20
    font_path = global_def.FONT_PATH
    font = ImageFont.truetype(font_path, font_size)

    image_width = 400
    line_height = 50
    
    total_height = line_height * len(object_list)
    result_image = Image.new("RGB", (image_width, total_height), color='white')
    draw = ImageDraw.Draw(result_image)

    image_text_distance = 10
    text_text_distance = 20

    image_path_prefix = ""
    if type == "ITEM":
        image_path_prefix = global_def.ITEM_SPRITE_PATH_PREFIX
    elif type == "TRINKET":
        image_path_prefix = global_def.TRINKET_SPRITE_PATH_PREFIX
    
    for index, object in enumerate(object_list):
        image_path = image_path_prefix + str(object.id) + global_def.PNG_SUFFIX
        if os.path.exists(image_path):
            img = Image.open(image_path).resize((32, 32))
        else:
            img = Image.new("RGB", (32, 32), color='gray') 

        y_position = index * line_height
        result_image.paste(img, (0, y_position + (line_height - 32) // 2))

        text_id = str(object.id)
        text_x_position = 32 + image_text_distance
        text_bbox = draw.textbbox((0, 0), text_id, font=font)
        # text_y_position = y_position + (line_height - (text_bbox[3] - text_bbox[1])) // 2
        text_y_position = y_position + 10
        draw.text((text_x_position, text_y_position), text_id, font=font, fill="black")
        
        text_name = str(object.name)
        text_name_x_position = text_x_position + (text_bbox[2] - text_bbox[0]) + text_text_distance
        draw.text((text_name_x_position, text_y_position), text_name, font=font, fill="black")

    result_image.save(global_def.VAGUE_SEARCH_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX)


def create_error_item_image(group_id):
    # 选择道具个数 2-7
    cover_num = random.randint(2, 7)
    logger.info(f"生成{cover_num}个图片")

    # 选择道具
    mix_items = []
    for i in range(cover_num):
        select = random.randint(1, 733)
        while select in mix_items or select in global_def.missing_item_number:
            select = random.randint(1, 733)
        mix_items.append(select)

    logger.info(str(mix_items))

    # 打开图片
    img_files = []
    for i in range(cover_num):
        img_fp = global_def.ITEM_SPRITE_PATH_PREFIX + str(mix_items[i]) + global_def.PNG_SUFFIX
        img_files.append(Image.open(img_fp))

    # 选择融合类型
    mix_type = random.randint(1, 2)

    # 竖排乱序
    if True:
        # 保证每一块大小至少为1
        remaining = 32 - 1 * cover_num
        parts = []
        dividers = sorted(random.sample(range(1, remaining), cover_num-1))
        prev = 0
        for d in dividers:
            parts.append(d - prev)
            prev = d
        parts.append(remaining - prev)
        
        widths = [4 + p for p in parts]
        new_img = img_files[0]
        current_x = 0
        
        for i in range(1, cover_num):
            img = img_files[i]
            w = random.randint(1, widths[i])
            max_x0 = 32 - w
            if max_x0 < 0:
                x0 = 0
            else:
                x0 = random.randint(0, max_x0)
            
            cropped = img.crop((x0, 0, x0 + w, 32))
            new_img.paste(cropped, (current_x, 0))
            current_x += widths[i]

        new_img.save(global_def.TMT_RES_PATH_PREFIX + str(group_id) + global_def.PNG_SUFFIX)
        

def dr_parse_image(month: int, day: int, filepath: str):
    file = Image.open(filepath)
    img_width, img_height = file.size

    cropped = file.crop(((month-1)*img_width/12, day*img_height/33, month*img_width/12, (day+1)*img_height/33))
    cropped.save(global_def.DR_TODAY_PATH)