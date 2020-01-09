# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # result = s = nums[0]
        res = list()
        res.append(nums[0])
        for i in range(1, len(nums)):
            # if s <= 0:
            #     s = nums[i]
            # else:
            #     s += nums[i]
            # if result < s:
            #     result = s
            # print(f'i: {nums[i]}, s:{s}, result:{result}')
            res.append(max(nums[i], nums[i] + res[-1]))  # 如果加上一个数之后比这个数本身还要小，则可以放弃这个数之前的加和结果
        return max(res)


so = Solution()
print(so.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))