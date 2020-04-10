# coding=utf-8
# builtins
# third party package
from kafka import KafkaProducer
# self built


if __name__ == "__main__":
    pro = KafkaProducer(bootstrap_servers="192.168.0.105:9092")
    for i in range(10):
        pro.send("test", str(i).encode())
        # pro.flush()