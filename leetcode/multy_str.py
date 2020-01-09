# coding=utf-8
# builtins
# third party package
# self built
def str_to_int(chars):
    l = len(chars)
    num = 0
    for i in range(l):
        num += (ord(chars[i]) - 48) * 10 ** (l - 1 - i)
    return num


def int_to_str(i):
    if i < 10:
        return chr(i + 48)
    z = i // 10
    s = chr(i % 10 + 48)
    return int_to_str(z) + s


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        num1 = str_to_int(num1)
        num2 = str_to_int(num2)
        print(num1, num2)
        return int_to_str(num1 * num2)

so = Solution()
print(so.multiply("123", "456"))
# print(int_to_str(56088))