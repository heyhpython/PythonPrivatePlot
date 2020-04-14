from typing import List


class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        sub_sum = k * threshold  # 子数组的和要大于这个数

        # 寻找长度为k且和大于等于sub_sum的子数组
        count = 0
        sum_start = sum(arr[:k])
        if sum_start >= sub_sum:
            count += 1
        for i in range(k, len(arr)):
            sum_start = sum_start-arr[i-k]+arr[i]
            if sum_start >= sub_sum:
                count += 1
            print(f"{i-k}-{i}={sum_start}")
        return count


if __name__ == "__main__":
    so = Solution()
    print(so.numOfSubarrays([2,2,2,2,5,5,5,8], 3, 4))
