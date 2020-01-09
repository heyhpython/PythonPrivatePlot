# coding=utf-8
'''
给定一个从1 到 n 排序的整数列表。
首先，从左到右，从第一个数字开始，每隔一个数字进行删除，直到列表的末尾。
第二步，在剩下的数字中，从右到左，从倒数第一个数字开始，每隔一个数字进行删除，直到列表开头。
我们不断重复这两步，从左到右和从右到左交替进行，直到只剩下一个数字。
返回长度为 n 的列表中，最后剩下的数字。
'''


def lastRemaining(n):
    return 1 if n == 1 else 2 * (n // 2 + 1 - lastRemaining(n // 2))
    step = 0
    while n // 2 >= 1:
        n = n // 2
        step += 1
    return step
    li = [i for i in range(1, n + 1)]

    while li.__len__() > 1:
        li = li[1::2][::-1]
        # print(li)
    return li[0]


for i in range(1, 90):
    print(lastRemaining(i))
print(lastRemaining(7))
