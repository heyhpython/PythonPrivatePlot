# coding=utf-8
# builtins
from typing import List
from functools import lru_cache
# third party package
# self built


class Solution:
    @lru_cache(maxsize=100)
    def solve(self, idx: int, nums: list):
        if idx < 0:
            return 0
        max_ = max(nums[idx] + self.solve(idx - 2, nums), self.solve(idx - 1, nums))
        return max_

    def rob(self, nums: List[int]) -> int:
        return self.solve(len(nums) - 1, nums)


so = Solution()
print(so.rob([1, 2, 3, 1]))