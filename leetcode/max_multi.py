# coding=utf-8
# builtins
from typing import  List
# third party package
# self built


class Solution:

    def maximumProduct(self, nums: List[int]) -> int:
        j, k, l = -1000, -1000, -1000  # num > 0 j<k<l
        m, n = 0, 0  # num < 0  |m| < |n|
        for num in nums:
            if num >= l:
                j, k, l = k, l, num
            elif num >= k:
                j, k = k, num
            elif num > j:
                j = num
            if num < 0:
                if num <= n:
                    m, n = n, num
                elif num < m:
                    m = num

        return max(j*k*l, m*n*l)


so = Solution()
print(so.maximumProduct([-1,-2,-3]))
