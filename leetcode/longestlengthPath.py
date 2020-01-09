# coding=utf-8
# builtins
import re
# third party package
# self built


# class Solution:
#
#     def solve(self, path, prefix,) -> int:
#         if '.' in path and '\t' not in path:
#             return len(prefix + f'/{path}')
#         elif '.' not in path and '\t' not in path :
#             return 0
#         if '\n' in path:
#             dir_name, *dirs = path.split('\n')
#         else:
#             dir_name, *dirs = path.split('\t')
#         print("dir_name:", dir_name)
#         print("dirs:", dirs)
#         res = []
#         for d in dirs:
#             if d.startswith('\t\t'):
#                 continue
#             res.append(self.solve(d, prefix=prefix+f'/{dir_name}'))
#         return max(res)
#
#     def lengthLongestPath(self, input: str) -> int:
#         return self.solve(input, '')

class Solution(object):
    def lengthLongestPath(self, input):
        """
        :type input: str
        :rtype: int
        """
        input = input.split('\n')
        print(input)
        res = 0
        stack = list()
        for i in input:
            d = i.count('\t')
            i = i[d:]
            print(len(stack), d)
            while len(stack) > d:
                stack.pop()
            if '.' in i:
                cur = len(i) + len(stack)
                for s in stack:
                    cur += len(s)
                res = max(res, cur)
            else:
                stack.append(i)
        return res

so = Solution()
print(so.lengthLongestPath('dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2'))
