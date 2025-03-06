from PIL import Image, ImageDraw, ImageFont
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


def create_error_item_image():
    # 选择道具个数 2-4
    cover_num = random.randint(2, 4)

    # 选择道具
    mix_items = []
    for i in range(cover_num):
        select = random.randint(1, 733)
        while select in mix_items or select in global_def.missing_item_number:
            select = random.randint(1, 733)

    # 打开图片
    