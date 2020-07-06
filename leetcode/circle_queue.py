# coding=utf-8
# builtins
# third party package
# self built


class MyCircularQueue:

    def __init__(self, k: int):
        """
        Initialize your data structure here. Set the size of the queue to be k.
        """
        self.data = [None for _ in range(k)]
        self.head = None
        self.tail = None
        self.size = k

    def enQueue(self, value: int) -> bool:
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        """
        if self.isFull():
            return False

        if self.head is None:
            self.head = 0
            self.tail = -1

        self.tail = (self.tail + 1) % self.size
        self.data[self.tail] = value
        # print(self.data, self.tail, "++++")
        return True

    def deQueue(self) -> bool:
        """
        Delete an element from the circular queue. Return true if the operation is successful.
        """
        if self.isEmpty():
            return False

        self.data[self.head] = None
        self.head = (self.head + 1) % self.size 
        return True

    def Front(self) -> int:
        """
        Get the front item from the queue.
        """
        return self.data[self.head] if not self.isEmpty() else -1

    def Rear(self) -> int:
        """
        Get the last item from the queue.
        """
        return self.data[self.tail] if not self.isEmpty() else -1

    def isEmpty(self) -> bool:
        """
        Checks whether the circular queue is empty or not.
        """
        for i in self.data:
            if i is not None:
                return False
        else:
            return True

    def isFull(self) -> bool:
        """
        Checks whether the circular queue is full or not.
        """
        for i in self.data:
            if i is None:
                return False
        else:
            return True


if __name__ == "__main__":
    queue = MyCircularQueue(6)
    print(queue.enQueue(6))
    print(queue.Rear())
    print(queue.Rear())
    print(queue.deQueue())
    print(queue.enQueue(5))
    print(queue.Rear())
    print(queue.deQueue())
    print(queue.Front())
    print(queue.deQueue())
    print(queue.deQueue())
    print(queue.deQueue())

