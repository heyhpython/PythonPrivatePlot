# coding=utf-8
# builtins
import glob
import logging
# third party package
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
# self built


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


lamp_classes = ["line", "circle", "None"]


# 数据集及处理
# 1. 将所有图片处理成指定的尺寸大小 如32*32等
# 2. 将训练与测试图片与其对应的分类做标记
# 如：(train_images, train_classes) （test_images, test_classes）
#  其中每一条训练数据、测试数据与其对应的分类是预先设计好的
#  即train_images 中的第一条的分类是train_classes中的第一条以此类推
#  train_images 是一个三位numpy数组 shape分别代表测试样本的数量,以及图片的每个像素

def load_data(s):
    """
    :param s: train or test
    :return:
    """
    # 读取数据集成numpy数组
    # 1000张800乘800的图
    files = glob.glob(f"./{s}*.*")
    print(files)
    images = np.zeros((len(files), 1000, 1000))
    classes = np.zeros((len(files)))
    i = 0
    for img_file_name in files:
        # 图片属于哪种类型在名称开头表示如train_line_1.jpg 表示训练集灯管的第一条数据是长条
        img = Image.open(img_file_name)
        img = img.crop((0, 0, 1000, 1000))
        img = img.convert('L')
        img = np.array(img)
        images[i] = img
        t, class_, _ = img_file_name.split('_')
        if class_ == "line":
            classes[i] = 0
        elif class_ == "circle":
            classes[i] = 1
        else:
            classes[i] = 2
        i += 1
    # 神经网络模型要求数据必须要0-1之间
    return images/255.0, classes


def main():
    # 组织训练集和测试集
    train_images, train_classes = load_data('train')
    logger.error(train_images)
    test_images, test_classes = load_data('test')

    # 建模
    # 网络的第一层将二维数据转化为一维 实现卷积层到全连接层的过渡
    # 第二和第三层是全连接神经网络层，第二层有128个节点 第三层返回一个长度为3的数组
    # 数组的每一个表示当前图形属于三类中某一类的logits(一个事件发生与该事件不发生的比值的对数)
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(1000, 1000)),  # 图片的尺寸
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(3)
    ])

    # 编译模型
    # optimizer 模型是根据丢失函数和数据由什么算法更新
    # 丢失函数度量模型训练期间的精度
    model.compile(
        optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        # loss=keras.losses.
    )

    # 训练模型
    # epochs 训练的代数
    model.fit(train_images, train_classes, epochs=6)

    # 精度测算
    logger.debug(model.evaluate(test_images,  test_classes, verbose=2))

    # 预测
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    # logger.debug(test_images)
    predictions = probability_model.predict(test_images)
    logger.debug(f"{predictions}")


def show_img(img_file_name):
    img = np.array(Image.open(img_file_name).convert('L'))
    print(img.shape)
    plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.imshow(img, cmap=plt.cm.binary)
    # plt.subplot(1, 2, 2)
    img = img/255.0
    plt.imshow(img/255.0, cmap=plt.cm.binary)
    plt.show()


if __name__ == "__main__":
    # show_img('./train_line_1.jpg')
    main()


