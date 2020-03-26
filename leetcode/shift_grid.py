from typing import List
from functools import reduce


class Solution:
    def shiftGrid(self, grid: List[List[int]],
                  k: int) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])
        grid = reduce(lambda a, b: a + b, grid)
        length = len(grid)
        k = k % length
        grid = grid[-k:] + grid[:length-k]
        return [grid[i*n: (i+1)*n] for i in range(m)]


so = Solution()
print(so.shiftGrid([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9))
print(so.shiftGrid([[3, 8, 1, 9], [19, 7, 2, 5],
                    [4, 6, 11, 10], [12, 0, 21, 13]], 4))
