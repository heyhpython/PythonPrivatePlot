from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        length = len(nums)
        for num in nums[:length//2+1]:
            if nums.count(num) >= length / 2:
                return num

if __name__ == "__main__":
    so = Solution()
    print(so.majorityElement([3,2,3]))
