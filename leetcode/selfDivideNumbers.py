# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    def selfDividingNumbers(self, left: int, right: int) -> List[int]:
        res = []
        for i in range(left, right + 1):
            if self.check_self_divide(i):
                res.append(i)
        return res

    @staticmethod
    def check_self_divide(num):
        if num <= 9:
            return True
        nums = set(str(num))
        if '0' in nums:
            return False
        mul = eval('*'.join(nums))
        return num % mul == 0
        # for n in nums:
        #     if num % int(n) != 0:
        #         return False
        # return True

so = Solution()
print(so.selfDividingNumbers(1, 22))
print(so.check_self_divide(48))