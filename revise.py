from PIL import Image
import os
import shutil
from tqdm import tqdm
def get_rightmost_black_column(img):

    for x in reversed(range(img.width)):
        is_black = True
        for y in range(img.height):
            pixel_value = img.getpixel((x, y))
            # Check if image is grayscale or RGB
            if isinstance(pixel_value, int):
                r = g = b = pixel_value
            else:
                r, g, b = pixel_value

            if r > 10 or g > 10 or b > 10:
                is_black = False
                break
        if not is_black:
            return x + 1
    return 0








def process_image(img_path, save_path, pad_width):
    img = Image.open(img_path)
    new_img = Image.new("L", (2294, 2294), "black")

    new_img.paste(img, (pad_width, 0))
    new_img.save(save_path)

# 指定文件夹路径
image_base_directory = "E:\cmmd1\image"
label_base_directory = "E:\cmmd1\label"
processed_image_directory = "E:\cmmd1\processed_image"
processed_label_directory = "E:\cmmd1\processed_label"

if not os.path.exists(processed_image_directory):
    os.makedirs(processed_image_directory)

if not os.path.exists(processed_label_directory):
    os.makedirs(processed_label_directory)


for sub_directory in tqdm(os.listdir(image_base_directory)):
    sub_directory_path = os.path.join(image_base_directory, sub_directory)
    new_image_sub_directory_path = os.path.join(processed_image_directory, sub_directory)
    new_label_sub_directory_path = os.path.join(processed_label_directory, sub_directory)

    if not os.path.exists(new_image_sub_directory_path):
        os.makedirs(new_image_sub_directory_path)
    if not os.path.exists(new_label_sub_directory_path):
        os.makedirs(new_label_sub_directory_path)

    if os.path.isdir(sub_directory_path):
        for filename in os.listdir(sub_directory_path):
            if filename.endswith('.png'):
                if "_R_" in filename:
                    img_path = os.path.join(sub_directory_path, filename)
                    img = Image.open(img_path)
                    pad_width = img.width - get_rightmost_black_column(img)

                   
                    process_image(img_path, os.path.join(new_image_sub_directory_path, filename), pad_width)

                    
                    label_directory = os.path.join(label_base_directory, sub_directory)
                    for label_filename in os.listdir(label_directory):
                        if label_filename.startswith(filename.split('.png')[0]):  
                            label_path = os.path.join(label_directory, label_filename)
                            process_image(label_path, os.path.join(new_label_sub_directory_path, label_filename), pad_width)
                elif "_L_" in filename:
                    
                    shutil.copy(os.path.join(sub_directory_path, filename), os.path.join(new_image_sub_directory_path, filename))

                    label_directory = os.path.join(label_base_directory, sub_directory)
                    for label_filename in os.listdir(label_directory):
                        if label_filename.startswith(filename.split('.png')[0]):  
                            shutil.copy(os.path.join(label_directory, label_filename), os.path.join(new_label_sub_directory_path, label_filename))
