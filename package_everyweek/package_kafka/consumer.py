# coding=utf-8
# builtins
# third party package
from kafka import KafkaConsumer
# self built
import os
os.getuid()

if __name__ == "__main__":
    com = KafkaConsumer("test", bootstrap_servers="192.168.0.105:9092")
    for msg in com:
        print(msg.value)