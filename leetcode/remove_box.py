from typing import List


class Solution:
    def removeBoxes(self, boxes: List[int]) -> int:
        length = len(boxes)
        dp = [[[None for i in range(length)] for j in range(length)] for k in range(length)]

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def solve(i, j, k):
            if i > j:
                return 0
            if dp[i][j][k] > 0:
                return dp[i][j][k]
            
            while 1:
                if i < j and boxes[i + 1] == boxes[i]:
                    break
                i += 1
                k += 1
            res = (k + 1)**2 + self.solve(boxes, i+1, j, 0, dp)

            for m in range(i+1, j+1):
                if boxes[i] == boxes[m]:
                    res = max(res, self.solve(boxes, i+1, m-1, 0, dp) + self.solve(boxes, m, j, k+1, dp))
            dp[i][j][k] = res
            return res
        return solve(0, length-1, 0)