# coding=utf-8
# builtins
# third party package
# self built

# 说明：
# ⦁    x为整数，-1e7 <= x <= 1e7;
# ⦁    操作次数不会超过10000;
# ⦁    当栈为空的时候，不会出现后四项操作。
#
# 答题区域：（正反面作答）


class MaxStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.data = list()

    def push(self, x: int) -> None:
        self.data.append(x)

    def pop(self) -> int:
        return self.data.pop(-1)

    def top(self) -> int:
        return self.data[-1]

    def peekMax(self) -> int:
        return max(self.data)

    def popMax(self) -> int:
        max_ = self.peekMax()
        idx = self.data[::-1].index(max_)
        return self.data.pop(len(self.data) - 1 - idx)


# Your MaxStack object will be instantiated and called as such:
from random import randint
obj = MaxStack()
for i in range(10):
    obj.push(randint(1, 100000))

param_2 = obj.pop()
param_3 = obj.top()
param_4 = obj.peekMax()
param_5 = obj.popMax()
print(param_2, param_3, param_4, param_5)