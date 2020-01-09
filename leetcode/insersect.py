# coding=utf-8
def intersect(nums1, nums2):
    if nums1 == [] or nums2 == []:
        return []

    d1 = {}
    for num in nums1:
        if num not in d1:
            d1[num] = 1
        else:
            d1[num] += 1

    d2 = {}
    for num in nums2:
        if num not in d2:
            d2[num] = 1
        else:
            d2[num] += 1

    ret = []

    for num in d1:
        if num not in d2:
            continue
        else:
            ret.extend([num for i in range(min(d1[num], d2[num]))])

    return ret


print(intersect([4,9, 5], [9,4,9,8,4]))

