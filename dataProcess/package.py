import numpy as np
from PIL import Image
import glob
import os

'''
TODO 
图片要求: 总文件夹下将不同类别的图片放在不同的文件夹中
将以下四个指标修改为自己需要的指标
标签会用数字的形式表现，数字i对应第i个文件夹的类别

最终会打包为一个npz文件，其中包含x_train, y_train, x_test, y_test，分别表示训练集，训练集标签(一维数组，标签顺序和训练集顺序一致)，测试集和测试标签
'''

# 图片总文件夹
dataset = './dataset/*'
# 类别数
classNum = 2
# 对于灰色图片是否扩展灰度通道，如果扩展将以(height,width,1)的形式保存，否则以(height,width)的形式保存
# 彩色图片请设置为false
isGray = True
# 每类测试集数量，请确保酶类的测试集数量小于该类别的总图片数
testRate = 20

'''
以下内容不需要修改
'''


dir_list = glob.glob(dataset)
train_set = [None]*classNum
test_set = [None]*classNum


def generate_pd(sub_list):
    res = None
    res_test = None
    j = 0
    for image_file_name in sub_list:
        image = Image.open(image_file_name)
        image_data = np.array(image)
        if(isGray): # 如果是单通道图像需要扩展一个维度
            image_data = np.expand_dims(image_data, axis=2)
        # 扩展第一个维度
        expand = np.expand_dims(image_data, axis=0)
        if j < testRate:
            if res_test is None:
                res_test = expand
            else:
                res_test = np.append(expand, res_test, axis=0)
        else:
            if res is None:
                res = expand
            else:
                res = np.append(expand, res, axis=0)
        j += 1
    return res, res_test

k = 0
for sub_dir in dir_list:
    sub_dir_all = sub_dir + '/*'
    sub_dir_list = glob.glob(sub_dir_all)
    train_set[k], test_set[k] = generate_pd(sub_dir_list)
    # generate_pd(sub_dir_list)
    k += 1

label = []

for i in range(classNum):
    for j in range(train_set[i].shape[0]):
        label.append(i)

y_train = np.array(label)
x_train = train_set[0]
k = 1
while k<classNum:
    x_train = np.append(x_train, train_set[k], axis=0)
    k += 1

label_test = []
for i in range(classNum):
    for j in range(test_set[i].shape[0]):
        label_test.append(i)

y_test = np.array(label_test)
x_test = test_set[0]

k = 1
while k<classNum:
    x_test = np.append(x_test, test_set[k], axis=0)
    k += 1

print('x_train大小:', x_train.shape, 'y_train大小:', y_train.shape, 'x_test大小:', x_test.shape, 'y_test大小:', y_test.shape)
print('每类图片总数:')

barr_train = 0
for i in range(classNum):
    num = 0
    while (barr_train<x_train.shape[0]):
        if y_train[barr_train]!=i:
            break
        barr_train += 1
        num += 1
    print('类别', i, '测试集数量', num)

np.savez('./data.npz', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

print('npz文件已保存至 ./data.npz\n请使用\ndata = np.load(\'data.npz\')\n(x_train, y_train, x_test, y_test) = (data[\'x_train\'], data[\'y_train\'], data[\'x_test\'], data[\'y_test\'])\n读取')



