# coding=utf-8
# builtins
# third party package
from tensorflow import keras
# self built


def main():
    fashion_mnist = keras.datasets.fashion_mnist
    (tr_images, tr_labels), (te_images, te_labels) = fashion_mnist.load_data()


if __name__ == "__main__":
    main()