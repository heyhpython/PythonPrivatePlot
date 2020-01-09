# coding=utf-8
# builtins
from typing import List
from collections import Counter
# third party package
# self built
from copy import deepcopy


class MajorityChecker_:
    """
    查找子数组里出现次数>=给出值的元素
    """

    def init__(self, arr: List[int]):
        length = len(arr)
        # dp 从索引left到right所有数出现的次数j
        # 比如dp[0][10]=[1,2,3,4] 表示从数组 0到10 ，0出现了1次 1出现了2次
        self.dp = [[dict() for i in range(length)] for j in range(length)]
        # print(self.dp)
        self.arr = arr

    def query_(self, left: int, right: int, threshold: int) -> int:
        self.solve(left, right)
        print(f"self.dp[left][right]={self.dp[left][right]}")
        for num, count in self.dp[left][right].items():
            if count >= threshold:
                return num
        else:
            return -1

    def solve_(self, left, right):
        if left < 0 or left > right:
            return
        print(f"arr[left:right] = {self.arr[left: right + 1]}")
        for i in range(left, right + 1):
            if self.dp[left][right].get(self.arr[i], None) is None:
                self.dp[left][right][self.arr[i]] = 1
            else:
                self.dp[left][right][self.arr[i]] += 1

    def __init__(self, arr: List[int]):
        self.result = {}
        self.arr = arr

    def solve(self, left, right) -> dict:
        print(f"result before[{left}:{right}]={self.result}")
        arr = self.arr[left: right + 1]
        self.result[f"{left}-{right}"] = dict(Counter(arr))
        print(f"result after[{left}:{right}]={self.result}")
        return dict(Counter(arr))

    def sub_result_from_result(self, left, right):
        # print(f"{left}-{right}result:{self.result}")
        for range_, result in self.result.items():
            l1, r1 = range_.split('-')
            l1, r1 = int(l1), int(r1)
            if l1 == left and r1 == right:
                return result
            if l1 < left or r1 > right:
                continue
            else:
                fore = self.sub_result_from_result(left, l1 - 1) if left < l1 else {}
                tail = self.sub_result_from_result(r1 + 1, right) if right > r1 else {}
                res = deepcopy(self.result[range_])
                print(f"fore[{left}:{l1 - 1}]:{fore};  res[{l1}：{r1}]:{res};  tail[{r1 + 1}:{right}]:{tail}")
                return self.result_add(self.result_add(fore, res), tail)

        else:
            return self.solve(left, right)

    def result_add(self, d1: dict, d2: dict) -> dict:
        print(f"result before add: {self.result}")
        print(f"dict need to be add {d1}+{d2}")
        d1, d2 = deepcopy(d1), deepcopy(d2)
        res = {}
        for k, c1 in d1.items():
            c2 = 0
            if k in d2:
                c2 = d2.pop(k)
            res[k] = c1 + c2
        res.update(d2)
        print(f"dict add res {res}")
        print(f"result after add: {self.result}")
        return res

    def query(self, left: int, right: int, threshold: int) -> int:
        print(f"arr[{left}:{right}]={self.arr[left:right + 1]}")
        res = self.result.get(f"{left}-{right}", None)
        if res is None:
            print(res)
            res = self.sub_result_from_result(left, right)
            self.result[f"{left}-{right}"] = res
            print(res)
        for num, count in res.items():
            if count >= threshold:
                return num
        else:
            return -1


# so = MajorityChecker([1, 1, 2, 2, 1, 1])
# print("++++++" * 20)
# print(f"so.query(0, 5, 4)={so.query(0, 5, 4)}")  # 1
# print("++++++" * 20)
# print(f"so.query(0, 3, 3)={so.query(0, 3, 3)}")  # -1
# print("++++++" * 20)
# print(f"so.query(2, 3, 2)={so.query(2, 3, 2)}")  # 2

class MajorityChecker:
    def __init__(self, arr: List[int]):
        self.nums = {}  # {1:[1,2,3]} 1出现在位置1 ， 2， 3
        self.arr = arr
        for i in range(len(arr)):
            if self.nums.get(arr[i], None) is None:
                self.nums[arr[i]] = [i]
            else:
                self.nums[arr[i]].append(i)

    def query(self, left: int, right: int, threshold: int) -> int:
        pass


nums = [1, 1, 2, 2, 1, 1]
cases = [[0, 5, 4], [0, 3, 3], [2, 3, 2]]

so = MajorityChecker(nums)
for l, r, t in cases:
    print("++++++" * 20)
    print(f"so.query({l}, {r}, {t})={so.query(l, r, t)}")
