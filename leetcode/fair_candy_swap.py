# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    def fairCandySwap(self, A: List[int], B: List[int]) -> List[int]:
        return self.solve(A, B)

    def solve(self, A: List[int], B: List[int]) -> List[int]:
        sum_a = sum(A)
        sum_b = sum(B)
        differ_ab = sum_a - sum_b
        for c in A:
            x = -(differ_ab - 2*c)//2
            if x in B:
                return [c, x]


if __name__ == "__main__":
    so = Solution()
    # A = [1, 1]
    # B = [2, 2]
    # A = [2]
    # B = [1, 3]
    A = [1, 2, 5]
    B = [2, 4]
    import cProfile

    print(so.solve(A, B))