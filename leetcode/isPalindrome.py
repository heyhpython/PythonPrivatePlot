def toScience(num):
    ret = []
    while num >= 10:
        ret.append(num % 10)
        num = num // 10
    ret.append(num)
    return ret


print(toScience(1001231))


def isPalindrome(x):
    num = x
    r=0
    while r<num:
        pass


print(isPalindrome(121))
