# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:
    minus = 100
    minus_idx = 0

    def shortestCompletingWord(self, licensePlate: str, words: List[str]) -> str:
        licensePlate = ''.join([c if c.isalpha() else'' for c in licensePlate]).lower()
        length = len(words)

        def solve(idx):
            if idx >= length:
                return
            word: str = words[idx]
            for c in licensePlate:
                print(f"c: {c}; word:{word}")
                if (c not in word) and (c.upper() not in word):
                    return solve(idx + 1)
                else:
                    print(f"c:{c} in word:{word}")
                    word = word.replace(c, '', 1)
            else:
                l = len(words[idx])
                if l < self.minus:
                    self.minus, self.minus_idx = (l, idx)
                return solve(idx + 1)

        solve(0)
        return words[self.minus_idx]

so = Solution()
print(so.shortestCompletingWord("1s3 PSt", ["step","steps","stripe","stepple"]))