# coding=utf-8
# builtins
# third party package
# self built


class Solution:
    def divisorGame(self, N: int) -> bool:
        # 爱丽丝为偶数 鲍博为奇数
        if N % 2 != 0:
            return False
        else:
            return True


so = Solution()
print(so.divisorGame(2))
print(so.divisorGame(3))
print(so.divisorGame(4))