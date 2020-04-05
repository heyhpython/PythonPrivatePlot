# coding=utf-8
# builtins
# third party package
# self built


class Solution:
    def binaryGap(self, N:int) -> int:
        bin_str = bin(N)[2:]
        m_gap = 0
        print(f"二进制字符串：{bin_str}")
        i, j = 0, 0
        while i < len(bin_str):
            if bin_str[i] == '1':
                for j in range(i+1, len(bin_str)):
                    if bin_str[j] == '1':
                        if (j - i) >= m_gap:
                            m_gap = j-i
                        i = j
                        print(f"i:{i}; str[i]:{bin_str[i]}; j:{j};str[j]:{bin_str[j]}; m_gap:{m_gap}")
                        break
                else:
                    return m_gap
            else:
                i += 1

        return m_gap

    def solve(self, N):
        bin_str = bin(N)[2:]
        m_gap = 0
        print(f"二进制字符串：{bin_str}")
        i, j = 0, 0
        for b in range(len(bin_str)):
            if bin_str[b] == '1':
                j = i
                i = b
                m_gap = max(m_gap, i-j)

        return m_gap


from leetcode import timer


@timer
def func1(N):
    bi = []
    while N != 1:
        bi.append(N % 2)
        N = N // 2
    bi += [1]
    bi.reverse()
    return bi

@timer
def func2(N):
    return bin(N)[2:]


def main(N):
    func1(N)
    func2(N)


if __name__ == "__main__":
    so = Solution()
    # print(so.binaryGap(22))
    # print(so.binaryGap(5))
    # print(so.binaryGap(6))
    # print(so.binaryGap(8))
    # print(so.solve(2897))
    # import cProfile
    # cProfile.run("main(123134124121231231231231231231231)")
    main(231412414124141414124124)