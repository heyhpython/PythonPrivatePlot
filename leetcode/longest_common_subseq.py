# coding=utf-8
# builtins
# third party package
# self built


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        l1 = len(text1)
        l2 = len(text2)
        c = [[0] * l2] * l1
        b = [[None] * l2] * l1
        for i in range(0, l1):
            for j in range(0, l2):
                if i == 0 or j == 0:
                    if text1[i] == text2[j]:
                        c[i][j] = 1
                else:
                    if text1[i] == text2[j]:
                        c[i][j] = c[i - 1][j - 1] + 1
                        b[i][j] = -1
                    else:
                        if c[i - 1][j] >= c[i][j - 1]:
                            c[i][j] = c[i - 1][j]
                            b[i][j] = 1
                        else:
                            c[i][j] = c[i][j - 1]
                            b[i][j] = 0
                print(f'text1[{i}]:{text1[i]}, text2[{j}]:{text2[j]}, c[{i}][{j}]:{c[i][j]}, b[{i}][{j}]:{b[i][j]}')
        return max([max(col) for col in c])



so = Solution()
# print(so.longestCommonSubsequence("ezupkr", "ubmrapg"))   # 2
print(so.longestCommonSubsequence("pmjghexybyrgzczy", "hafcdqbgncrcbihkd"))
# print(so.longestCommonSubsequence("abcde", "ace"))   # 3
