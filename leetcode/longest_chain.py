from typing import List

class Solution:

    def findLongestChain(self, pairs: List[List[int]]) -> int:
        pairs.sort(key=lambda x: x[1])
        print(pairs)
        cur, ans = -float('inf'), 0
        for fore, end in pairs:
            if cur < fore:
                ans += 1
                cur = end
        return ans


so = Solution()
print(so.findLongestChain([[1, 2], [2, 3], [3, 4], [5, 6]]))
# print(so.findLongestChain([[-10,-8],[8,9],[-5,0],[6,10],[-6,-4],[1,7],[9,10],[-4,7]]))