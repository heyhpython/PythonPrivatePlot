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
import jieba
# self built
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


# 1.对词汇进行编码 比如1：世界， 那么一句话经过分词之后就可以转化为一个一维不定长度的数组
# 2.将一维数组转化为结构类似的张量 比如多维向量（耗费内存） 或者填充数组使不同长度的评论得到的数组长度相同
# 3.建模
vocab_size = 10000

model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 16),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

