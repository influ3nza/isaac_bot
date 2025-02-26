from PIL import Image, ImageDraw, ImageFont
import os

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
        file_path = f'../tools/item_sprite/item_sprite_{num}.png'
        
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