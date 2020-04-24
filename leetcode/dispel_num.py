# coding=utf-8
# builtins
# third party package
# self built
#
# 返回两次操作后，数组元素之和的最小值
# @param nums int整型一维数组 这你你需要操作的数组
# @return long长整型
#


class Solution:
    def minimumValueAfterDispel(self, nums):
        nums1 = self.solve_once(nums)
        # print(nums1)
        nums2 = self.solve_once(nums1)
        print(sum(nums2))

    def solve_once(self, nums):
        nums.sort()
        s = sum(nums)
        res = float('inf')
        n = None
        for i in range(min(nums), max(nums) + 1):
            idx = None
            for j in range(len(nums)):
                # 找到目标数载数组中的位置
                num = nums[j]
                if num >= i:
                    idx = j
                    break
            tem = s - len(nums[idx:]) * i
            if tem < res:
                # print(f"i:{i}, idx:{idx}，num:{nums[idx]}")
                res = tem
                n = nums[idx]
        return [num - n if num >= n else num for num in nums]

# so = Solution()
# so.minimumValueAfterDispel([1, 3, 2, 0, 3])
# so.minimumValueAfterDispel([2, 1, 3])


class Solution:
    def countLR(self, a, b):
        # write code here
        length = len(a)
        c = 0
        s_a = dict()
        for l in range(length):
            for r in range(l, length):
                sl = s_a.get(l)
                if not sl:
                    sl = sum(a[:l+1])
                    s_a[l] = sl
                sr = s_a.get(r)
                if not sr:
                    sr = sum(a[:r+1])
                    s_a[r] = sr
                if sr - sl + a[l] == b[l] + b[r]:
                    c += 1
        print(c)

# Solution().countLR([1,2,3,4], [2,1,4,5])
Solution().countLR([52,3,65,78,0,69,87,79,44,54,85,8,6,35,25,84,66,77,12],[79,1367,942,757,864,1871,1379,5,640,1691,1585,1167,448,1819,2,573,260,918,724])