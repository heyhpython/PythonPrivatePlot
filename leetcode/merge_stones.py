from typing import List


class Solution:
    def mergeStones(self, stones: List[int], K: int) -> int:
        return self.solve(stones, K) if self.check_ava(len(stones), K) else -1

    def solve(self, stones: List[int], K: int):
        print(f"stones:{stones}, k:{K}")
        length = len(stones)
        if length == 1:
            return 0
        elif length == K:
            return sum(stones)
        # return min([sum(stones[i: i+3]) + self.solve(stones[:i] + [sum(stones[i: i+3])] + stones[i+3:], K) for i in range(0, length-K+1)])
        res = []

        for i in range(0, length-K+1):
            tem_sum = sum(stones[i: i+K])
            res.append(
                tem_sum + self.solve(stones[:i] + [tem_sum] + stones[i+K:], K))
        return min(res)

    @staticmethod
    def check_ava(length, K):
        while length >= K:
            length = length % K + length // K
        else:
            return False if length != 1 else True


if __name__ == "__main__":
    so = Solution()
    # print(so.check_ava(4, 1))
    # print(so.mergeStones([3, 2, 4, 1], 3))
    # print(so.mergeStones([3, 2, 4, 1], 2))
    # print(so.mergeStones([5, 4, 1], 2))
    # print(so.mergeStones([3, 5, 1, 2, 6], 3))
    print(so.mergeStones(
        [69, 39, 79, 78, 16, 6, 36, 97, 79, 27, 14, 31, 4], 2))
