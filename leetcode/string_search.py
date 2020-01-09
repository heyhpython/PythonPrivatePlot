# coding=utf-8
# builtins
# third party package
# self built


def search(s: str, p: str):
    lp = len(p)
    ls = len(s)
    n = lp

    while n < ls:
        cur_str = s[n-lp:n]
        i = 1
        idx_shift = 0
        while i < lp:
            i += 1
            if cur_str[lp - i] != p[lp - i]:
                idx_shift = i - cur_str[::-1].index(cur_str[lp - i])
                n += idx_shift
                break
        if idx_shift == 0:
            break

    return n - lp


print(search('here is example a simple example', 'example'))
