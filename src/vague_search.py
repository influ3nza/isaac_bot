from PIL import Image, ImageDraw, ImageFont
import os

from .global_def import FONT_PATH, VAGUE_SEARCH_RES_PATH

def create_image_with_list(item_list):
    font_size = 20
    font_path = FONT_PATH
    font = ImageFont.truetype(font_path, font_size)

    image_width = 400
    line_height = 50
    
    total_height = line_height * len(item_list)
    result_image = Image.new("RGB", (image_width, total_height), color='white')
    draw = ImageDraw.Draw(result_image)

    image_text_distance = 10
    text_text_distance = 20
    
    for index, item in enumerate(item_list):
        image_path = f"../tools/item_sprite/item_sprite_{item.id}.png"
        if os.path.exists(image_path):
            img = Image.open(image_path).resize((32, 32))
        else:
            img = Image.new("RGB", (32, 32), color='gray')  # Use gray placeholder if not found

        y_position = index * line_height
        result_image.paste(img, (0, y_position + (line_height - 32) // 2))

        text_id = str(item.id)
        text_x_position = 32 + image_text_distance
        text_bbox = draw.textbbox((0, 0), text_id, font=font)
        # text_y_position = y_position + (line_height - (text_bbox[3] - text_bbox[1])) // 2
        text_y_position = y_position + 10
        draw.text((text_x_position, text_y_position), text_id, font=font, fill="black")
        
        text_name = str(item.name)
        text_name_x_position = text_x_position + (text_bbox[2] - text_bbox[0]) + text_text_distance
        draw.text((text_name_x_position, text_y_position), text_name, font=font, fill="black")

    result_image.save(VAGUE_SEARCH_RES_PATH)