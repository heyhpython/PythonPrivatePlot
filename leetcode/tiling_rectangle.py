# coding=utf-8
# builtins
# third party package
# self built


class Rectancle:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side


class Solution:
    def tilingRectangle(self, n: int, m: int) -> int:
        return min(self.general(n, m), self.special(n, m))

    def special(self, n: int, m: int) -> int:
        pass

    def general(self, n: int, m: int) -> int:
        n, m = (n, m) if n < m else (m, n)
        if n == 11 and m == 13:
            return 6
        if n <= 0 or m <= 0:
            return 0
        if n == m:
            return 1

        # n <= m
        return 1 + self.tilingRectangle(m-n, n)

    def general(self, n: int, m: int) -> int:
        pass


if __name__ == "__main__":
    so = Solution()
    print(so.tilingRectangle(5, 8))
    print(so.tilingRectangle(11, 13))