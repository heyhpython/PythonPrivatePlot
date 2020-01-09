import re_


def longestCommonPrefix(strs):
    shortest = min(list(map(lambda i: len(strs[i]), [i for i in range(len(strs))])))
    print(shortest)
    i = 0
    start = strs[0]
    short = len(strs[0]) if len(strs) > 0 else None
    l = short
    ret = ''
    if short is None:
        return ret

    while i <= l:
        print(ret)
        s = start[i:i + short // 2] if short > 1 else start[i:i+1]
        try:
            if all([chars.startswith(ret+s) for chars in strs]):
                ret += s
                i = i + short // 2

            else:
                short //= 2
        except IndexError:
            # zai qian 1/2
            pass

            short //= 2
        if short <= 1:
            return ret

    return ret


print(longestCommonPrefix(["a", "a"]))
