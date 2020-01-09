# coding=utf-8
# builtins
from typing import List
# third party package
# self built

class Solution:

    def get_middle(self, nums):
        l = len(nums)
        if l == 0:
            return
        elif l == 1:
            return nums[0]
        return nums[l // 2]

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        return (self.get_middle(nums1) + self.get_middle(nums2)) / 2


so = Solution()
print(so.findMedianSortedArrays([1, 2], [3, 4]))