# 主要实现数据集扩展
from keras.preprocessing import image
import os

# ----------------------------------------------- 请根据需要修改以下参数 ------------------------------------------------

'''
输入图片目录 -- 注意该目录下还需要有分类的文件夹，例如 in_path = './test',则图片应该存储在 ./test/Subdirectory/ 路径下，
因为keras.preprocessing模块需要检测到图片类别才能处理图片
'''
in_path = './gesture/dataset'
# 输出图片目录
out_path = './test/gen/bazhang'

# 输出图片宽度
image_width = 324
# 输出图片高度
image_height = 244
# 旋转范围（角度制），例如 rotation_range = 90 表示旋转角度的范围是 0-90 度
rotation_range = 90
# 横向平移范围（比例）
width_shift_range = 0.3
# 纵向平移范围
height_shift_range = 0.3
# 保存新图片的前缀
prefix = 'gen'
# 生成倍数，gen_num = 50 表示生成原图数量50倍的数据集
gen_num = 20
# 保存格式
s_format = 'ppm'
# 保存为彩色或灰色 ，灰色为 grayscale ， 彩色为 rgb 或 rgba
color = 'grayscale'
# ----------------------------------------------- 以下内容无需修改 ------------------------------------------------


# 递归查询文件夹下的文件个数
def cal_file_num(directory):
    content = os.listdir(directory)
    total_count = 0
    for lists in content:
        sub_path = os.path.join(directory, lists)
        if os.path.isfile(sub_path):
            total_count += 1
        elif os.path.isdir(sub_path):
            temp = cal_file_num(sub_path)
            total_count += temp
    return total_count


image_num = cal_file_num(in_path)


# 旋转处理，angle为旋转的角度范围
def rotate(angle):
    datagen = image.ImageDataGenerator(rotation_range=angle)
    gen_data = datagen.flow_from_directory(in_path, batch_size=1, shuffle=False, save_to_dir=out_path
                                           , save_prefix=prefix, target_size=(image_height, image_width)
                                           , save_format=s_format, color_mode=color)
    for i in range(gen_num*image_num):
        gen_data.next()


# 横向平移处理，pixel为平移的比例范围
def width_shift(pixel):
    datagen = image.ImageDataGenerator(width_shift_range=pixel)
    gen_data = datagen.flow_from_directory(in_path, batch_size=1, shuffle=False, save_to_dir=out_path
                                           , save_prefix=prefix, target_size=(image_height, image_width)
                                           , save_format=s_format, color_mode=color)
    for i in range(gen_num*image_num):
        gen_data.next()


# 纵向平移处理，pixel为平移的比例范围
def height_shift(pixel):
    datagen = image.ImageDataGenerator(height_shift_range=pixel)
    gen_data = datagen.flow_from_directory(in_path, batch_size=1, shuffle=False, save_to_dir=out_path
                                           , save_prefix=prefix, target_size=(image_height, image_width)
                                           , save_format=s_format, color_mode=color)
    for i in range(gen_num*image_num):
        gen_data.next()


rotate(rotation_range)
width_shift(width_shift_range)
height_shift(height_shift_range)
