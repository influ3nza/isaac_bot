from PIL import Image, ImageDraw, ImageFont
import os
import random

from . import global_def

def generate_image_sequence_down(id):
    x = id - 5
    numbers = list(range(x, id + 1))

    numbers = [num for num in numbers if num > 0]

    if 668 in numbers:
        numbers = [num for num in numbers if num >= 668]

    return numbers

def generate_image_sequence_up(id):
    x = id + 5
    numbers = list(range(id, x + 1))

    numbers = [num for num in numbers if num > 0]

    if 668 in numbers:
        numbers = [num for num in numbers if num <= 668]

    return numbers

def create_concatenated_image(id_sequence, pathname):
    image_list = []
    for num in id_sequence:
        file_path = f'./tools/item_sprite/item_sprite_{num}.png'
        
        if os.path.exists(file_path):
            try:
                img = Image.open(file_path)
                image_list.append(img)
            except Exception as e:
                print(f"Could not open image {file_path}: {e}")
        else:
            print(f"Image file {file_path} not found.")

    if image_list:
        total_width = sum(img.width for img in image_list)
        max_height = max(img.height for img in image_list)

        result_img = Image.new('RGBA', (total_width, max_height))

        x_offset = 0
        for img in image_list:
            result_img.paste(img, (x_offset, 0))
            x_offset += img.width

        result_img.save(pathname)
    else:
        print("No images were loaded to create the output image.")


def create_blurred_sprite(id: int):
    file_path = f'./tools/item_sprite/item_sprite_{id}.png'

    img = Image.open(file_path).convert('RGBA')
    a = 8
    
    # 预处理alpha通道矩阵和积分图
    pixels = img.load()
    alpha = []
    for i in range(32):
        row = []
        for j in range(32):
            alpha_val = pixels[i, j][3]
            row.append(1 if alpha_val == 0 else 0)
        alpha.append(row)
    
    # 计算积分图
    integral = [[0] * 33 for _ in range(33)]
    for i in range(32):
        for j in range(32):
            integral[i+1][j+1] = alpha[i][j] + integral[i][j+1] + integral[i+1][j] - integral[i][j]
    
    max_attempts = 1000  # 最大尝试次数
    for cnts in range(max_attempts):
        # 随机生成区域的左上角坐标
        x = random.randint(4, 28 - a)
        y = random.randint(4, 28 - a)
        x_end = x + a - 1
        y_end = y + a - 1
        
        # 计算透明像素数量
        total_transparent = integral[x_end+1][y_end+1] - integral[x][y_end+1] - integral[x_end+1][y] + integral[x][y]
        if total_transparent / (a * a) <= 0.3 or cnts == max_attempts-1:
            # 截取区域并调整大小
            cropped = img.crop((x, y, x + a, y + a))
            resized = cropped.resize((128, 128), Image.Resampling.LANCZOS)

            # 增加难度：旋转
            ran_rot = random.randint(1, 4)
            if ran_rot == 2: 
                resized = resized.rotate(90, expand=True)
            if ran_rot == 3:
                resized = resized.rotate(180, expand=True)
            if ran_rot == 4:
                resized = resized.rotate(270, expand=True)

            resized.save(global_def.SPRITE_GUESS_PATH)
            return