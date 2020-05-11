# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        nums = [str(num) for num in nums]
        for i in range(len(nums) -1):
            for j in range(i+1, len(nums)):
                if (nums[i]+nums[j]) < (nums[j] + nums[i]):
                    nums[i], nums[j] = nums[j], nums[i]
        return ''.join(nums)

    def solve(self, nums: List[int]) -> str:
        class Mystr(str):
            def __lt__(self, other):
                return self + other < other + self

            def __gt__(self, other):
                return not self.__lt__(other)

        return str(int(''.join(sorted(map(Mystr, nums), reverse=True))))

so = Solution()
so.largestNumber([3,30,34,5,9])
print(so.solve([3,30,34,5,9]))
# 输出: 9534330)
