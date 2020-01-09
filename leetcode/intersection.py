# coding=utf-8
def intersection(nums1, nums2):
    qs = lambda nums: nums if len(nums) <= 1 else qs([i for i in nums[1:] if i < nums[0]]) + [nums[0]] + qs(
        [i for i in nums[1:] if i > nums[0]])

    nums1 = qs(nums1)
    nums2 = qs(nums2)
    print(nums1)
    print(nums2)
    d = {i: 1 for i in nums1}
    ret = []
    for num in nums1:
        if num in d:
            d[num] += 1
            ret.append(d[num])
        if num > nums1[-1]:
            break
    return ret


print(intersection([1, 2, 2, 1], [2, 2]))
