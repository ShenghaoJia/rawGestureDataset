# 处理ppm图片边缘的黑色像素
from PIL import Image
import os

# 批量处理图片的输入目录
in_directory = './gesture/bazhang'
# 处理后的输出目录
out_directory = './gesture/dataset/bazhang'
# directory = './gesture/bazhang'

# -------------------------- 以下内容无需修改 ------------------------------

content = os.listdir(in_directory)
for lists in content:
    sub_path = os.path.join(in_directory, lists)
    if os.path.isfile(sub_path):
        img = Image.open(sub_path)
        w, h = img.size
        x = 1
        y = 1
        # print(w,"   ",h)
        while x < w-1:
            img.putpixel((x, 0), img.getpixel((x, 1)))
            img.putpixel((x, h-1), img.getpixel((x, h-2)))
            x += 1
        while y < h - 1:
            img.putpixel((0, y), img.getpixel((1, y)))
            img.putpixel((w-1, y), img.getpixel((w-2, y)))
            y += 1
        img.putpixel((0, 0), img.getpixel((1, 1)))
        img.putpixel((0, h-1), img.getpixel((1, h-2)))
        img.putpixel((w-1, 0), img.getpixel((w-2, 1)))
        img.putpixel((w-1, h-1), img.getpixel((w-2, h-2)))
        save_path = os.path.join(out_directory, lists)
        img.save(save_path)