def intToRoman(num):
    num = [int(i) for i in str(num)]
    '''I
    1
    V
    5
    X
    10
    L
    50
    C
    100
    D
    500
    M
    1000'''
    length = len(num)
    ret = ''
    for i in range(length):
        k = 10 ** (length - i - 1)
        n = num[i]
        if k == 1000:
            for i in range(n):
                ret += 'M'
        elif k == 100:
            if n == 9:
                ret += 'CM'
            elif 5 <= n <= 8:
                ret += 'D'
                for i in range(n - 5):
                    ret += 'C'
            elif n == 4:
                ret += 'CD'
            elif 1 <= n < 4:
                for i in range(n):
                    ret += 'C'
        elif k == 10:
            if n == 9:
                ret += 'XC'
            elif 5 <= n <= 8:
                ret += 'L'
                for i in range(n - 5):
                    ret += 'X'
            elif n == 4:
                ret += 'XL'
            elif 1 <= n < 4:
                for i in range(n):
                    ret += 'X'
        elif k == 1:
            if n == 9:
                ret += 'IX'
            elif 5 <= n <= 8:
                ret += 'V'
                for i in range(n - 5):
                    ret += 'I'
            elif n == 4:
                ret += 'IV'
            elif 1 <= n < 4:
                for i in range(n):
                    ret += 'I'
    return ret


# print(intToRoman(10))

def romanToInt(s):
    '''
    I 1
    V 5
    X 10
    L 50
    C 100
    D 500
    M 1000'''
    d = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    i = 0
    ret = 0
    while i < len(s):
        c = s[i]
        next = s[i + 1]
        if d.get(c) < d.get(next):
            ret += d.get(next)
            ret -= d.get(c)
            i += 2
        else:
            ret += d.get(c)
            i += 1
    return ret

print(romanToInt('IX'))
