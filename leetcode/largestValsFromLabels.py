# coding=utf-8
# builtins
from typing import List
# third party package
# self built


class Solution:

    def largestValsFromLabels(self, values: List[int], labels: List[int],
                              num_wanted: int, use_limit: int) -> int:
        """
        选出num_wanted个数，其中每个数的标签最多可可出现use_limit次，返回这些书最大的和
        :param values:
        :param labels:
        :param num_wanted:
        :param use_limit:
        :return:
        """
        data = self.sort_value_label(values, labels)
        print(data)
        i = 0
        s = 0
        nums_in = 0
        labels_in = []
        while i < len(values) and nums_in < num_wanted:
            d, l = data[i]
            if labels_in.count(l) >= use_limit:

                i += 1
                continue
            else:
                s += d
                nums_in += 1
                labels_in.append(l)
                i += 1
        return s, nums_in, labels_in

    @staticmethod
    def sort_value_label(values, labels):
        data = [0]*len(values)
        for i in range(len(values)):
            data[i] = (values[i], labels[i])
        # 由大到小排序
        data = sorted(data, key=lambda d: d[0], reverse=True)
        return data


so = Solution()
so.sort_value_label([5, 4, 3, 2, 1], [1, 1, 2, 2, 3])
print(so.largestValsFromLabels([5, 4, 3, 2, 1], [1, 1, 2, 2, 3], 3, 1))