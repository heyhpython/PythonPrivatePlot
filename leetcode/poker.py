# coding=utf-8
# builtins
# third party package
# self built

m = None  # i, j的最小值


def deal(nums):
    l = len(nums)
    global m
    m = [[None for i in range(l)] for j in range(l)]
    for i in range(0, l):
        m[i][i] = nums[i]
        for j in range(i, l):
            print(f'i:{i}, j:{j} m:{m}')
            if not m[i][j]:
                min_ = min(nums[i: j+1])
                m[i][j] = min_
                # print(f'nums[{i}:{j}]:{nums[i:j+1]}, min:{min_}, m[{i}][{j}]:{m[i][j]}')


def solve(nums, s, e):
    deal(nums)
    if s > e:
        s, e = e, s
    print(f'm:{m} \nm[{s}][{e}]:{m[s][e]}')
    return m[s][e]


print(solve([1, 2, 3, 4, 1, 2, 3, 4], 0, 7))