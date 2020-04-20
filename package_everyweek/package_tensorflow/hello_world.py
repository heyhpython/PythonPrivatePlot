# coding=utf-8
# builtins
# third party package
# self built

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow import optimizers


class_names = ['line', 'circle', 'None']


def main():
    mnist = keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, y_train = x_train/255.0, y_train/255.0  # 将训练集与测试及的数据都转到0-1之间

    # 搭建模型
    model = keras.models.Sequential([
        layers.Flatten(input_shape=(28, 28)),  # 模型层从数据中提取代表性信息，通常这些信息对于所要解决的问题都有意义
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',  # 优化器 tf.keras.optimizers
                  loss='sparse_categorical_crossentropy',  # 损失函数tf.keras.losses
                  metrics=['accuracy']
                  )

    # 训练并验证模型
    model.fit(x_train, y_train)
    model.evaluate(x_test, y_test, verbose=2)


if __name__ == "__main__":
    main()