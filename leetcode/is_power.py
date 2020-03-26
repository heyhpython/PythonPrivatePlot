class Solution:
    def isPowerOfFour(self, num: int) -> bool:
        return print(self.is_power(num, 4))

    def is_power(self, num1, num2):
        # num1是否是num2的幂次方
        while 1:
            num1 = num1 / num2
            if num1 == num2:
                return True
            elif num1 < num2 and num2 != 1:
                return False


if __name__ == "__main__":
    so = Solution()
    so.isPowerOfFour(16)
    so.isPowerOfFour(1)
