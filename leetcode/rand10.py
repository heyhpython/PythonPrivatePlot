# The rand7() API is already defined for you.
from random import randint


def rand7():
    return randint(1, 7)


class Solution:

    def rand10(self):
        """
        :rtype: int
        """
        r7_1 = rand7()
        r7_2 = rand7()
        idx = (r7_2-1) * 7 + r7_1
        if idx > 40:
            return self.rand10()
        else:
            return idx % 10 + 1


so = Solution()
for i in range(10):
    print(so.rand10())