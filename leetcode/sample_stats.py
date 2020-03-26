# coding=utf-8
# builtins
from typing import List


# third party package
# self built

class Solution:
    """返回最小值、最大值、平均值、中位数和众数"""
    def sampleStats(self, count: List[int]) -> List[float]:
        min_value = float('inf')
        max_value = -float('inf')
        sum_ = 0
        total_count = sum(count)
        mid_left_idx = total_count // 2
        mid_right_idx = total_count // 2 + 1
        print(mid_left_idx, mid_right_idx)
        mid_left = None
        mid_right = None
        cur_count = 0
        for num in range(256):
            if count[num] == 0:
                continue
            min_value = num if num < min_value else min_value  # 最小值
            max_value = num if num > max_value else min_value  # 最大值
            sum_ += num * count[num]  # 求和
            if cur_count < mid_left_idx <= (cur_count + count[num]) and mid_left is None:
                # 中位数
                print(f"num:{num}; mid_left:{mid_left}; mid_right:{mid_right}; cur_count:{cur_count}; count:{count[num]}")
                mid_left = num
            if cur_count < mid_right_idx <= (cur_count + count[num]) and mid_right is None:
                # 中位数
                print(f"num:{num}; mid_left:{mid_left}; mid_right:{mid_right}; cur_count:{cur_count}; count:{count[num]}")
                mid_right = num
            cur_count += count[num]
            # print(f"num:{num}; mid_left:{mid_left}; mid_right:{mid_right}")
        return [min_value, max_value, sum_/total_count, (mid_right + mid_left) / 2, count.index(max(count))]

    def solve(self, count: List[int]) -> List[float]:
        # 超出内存限制
        nums = list()
        [nums.extend([num] * count[num]) for num in range(len(count))]
        length = len(nums)
        print(nums)
        print(length)
        mid_idx = length // 2
        if length % 2 == 0:
            mid = (nums[mid_idx] + nums[mid_idx - 1]) / 2
        else:
            mid = nums[mid_idx + 1]
        return [nums[0], nums[-1], sum(nums)/length, mid, count.index(max(count))]


so = Solution()
nums = [0, 1, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(so.sampleStats(nums))  # [1, 2, 2, 2, 3, 3, 3, 3]
