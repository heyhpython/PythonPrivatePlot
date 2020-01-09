# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    def findTargetSumWays(self, nums: List[int], S: int) -> int:
        """
        给nums里的数标记正负，使数组和为s，找出共有多少种添加方法
        :param nums: lenght <=20 非空 sum不大于1000
        :param S:
        :return:count
        """
        # 假设正子集为p
        sum_ = sum(nums)
        p_sum = sum_ + S
        if sum_ < S or p_sum % 2 != 0:
            return 0
        p_sum = p_sum // 2
        dp = [0] * (p_sum + 1)
        dp[0] = 1
        for num in nums:
            # 每一遍循环得到和值为i的方法数，以次更新
            for i in range(p_sum, num - 1, -1):
                dp[i] += dp[i - num]
        return dp[p_sum]


so = Solution()
print(so.findTargetSumWays([1, 1, 1, 1, 1], 3))
