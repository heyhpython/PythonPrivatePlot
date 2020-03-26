from typing import List

class Solution:
    def sumZero(self, n: int) -> List[int]:
        res = list()
        seed = 1
        cur = None
        while 1:
            for i in range(1, n):
                if cur is None:
                    cur = seed-n
                else:
                    if cur <=0:
                        cur = 1 - cur
                    else:
                        cur = - cur - seed
                res.append(cur)
            rest = 0 -sum(res)
            if rest in res:
                # print(res, rest)
                res.clear()
                seed += 1
                continue
            else: 
                res.append(0-sum(res))
                break
        return res

if __name__ == "__main__":
    so = Solution()
    for i in range(1, 10):
        print(so.sumZero(i))