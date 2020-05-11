# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        i = 0
        res = list()
        length = len(nums)
        while i < (length - k + 1):
            temp_nums = nums[i: i+k]
            temp = max(temp_nums)
            max_idx = temp_nums.index(temp)
            print(i, max_idx)
            if max_idx > 0 and (i+k+max_idx) < length and max(nums[i+k:i+k+max_idx]) <= temp:
                i += max_idx
                res.extend([temp for _ in range(max_idx)])
            else:
                res.append(temp)
                i += 1

        return res

    def solve(self, nums: List[int], k: int) -> List[int]:
        length = len(nums)
        res = list()
        for i in range(0, length-k+1):
            res.append(max(nums[i:i+k]))
        return res

    def simple(self, nums: List[int], k: int) -> List[int]:
        win, ret = [], []
        for i, v in enumerate(nums):
            if i >= k and win[0] <= i - k:
                win.pop(0)
            while win and nums[win[-1]] <= v:
                # 如果最近添加的比当前值要小 舍弃
                win.pop()
            win.append(i)
            if i >= k - 1:
                ret.append(nums[win[0]])
        return ret

so = Solution()
print(so.solve([1,3,-1,-3,5,3,6,7], 3))
print(so.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3))
print(so.simple([1,3,-1,-3,5,3,6,7], 3))