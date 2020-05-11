# coding=utf-8
# builtins
from typing import List
# third party package
# self built
# 如果出现下述两种情况，交易 可能无效：
#
# 交易金额超过 ¥1000
# 或者，它和另一个城市中同名的另一笔交易相隔不超过 60 分钟（包含 60 分钟整）
# 每个交易字符串 transactions[i] 由一些用逗号分隔的值组成，这些值分别表示交易的名称，时间（以分钟计），金额以及城市。
#
# 给你一份交易清单 transactions，返回可能无效的交易列表。你可以按任何顺序返回答案。


class Solution:
    def invalidTransactions(self, transactions: List[str]) -> List[str]:
        # 名称、时间、金额、城市
        res = []
        trans_dict = {}
        for t in transactions:
            name, at, amount, city = t.split(',')
            # at, amount = float(at), float(amount)
            if float(amount) > 1000:
                # 剔除金额超限
                res.append(t)
            if name not in trans_dict:
                trans_dict[name] = [[name, at, amount, city]]
            else:
                trans_dict[name].append([name, at, amount, city])

        for name, trans in trans_dict.items():
            if len(trans) == 1:
                res.append(','.join(trans[0]))
                continue
            i = 0
            while i < len(trans):
                tran = trans[i]
                # print(tran)
                if tran is None:
                    continue
                _, ct_at, _, ct_city = tran
                found = False
                j = 0
                while j < len(trans):
                    if i == j:
                        j += 1
                        continue
                    o_tran = trans[j]
                    _, ot_at, _, ot_city = o_tran
                    if abs(float(ct_at)-float(ot_at)) <= 60 and ct_city != ot_city:
                        found = True
                        break
                if found:
                    res.append(','.join(tran))
                i += 1
        return res

    def solve(self, transactions):
        trans_dict = dict()
        res = []
        for t in transactions:
            # name, at, amount, city = t.split(',')
            info = t.split(',')
            if float(info[2]) > 1000:
                continue
            if info[0] not in trans_dict:
                trans_dict[info[0]] = [info]
            else:
                trans_dict[info[0]].append(info)

        for name, trans in trans_dict.items():
            if len(trans) == 1:
                res.append(','.join(trans[0]))
            i = 0
            while i < len(trans):
                tran = trans[i]
                i += 1
                _, at, amount, city = tran
                for ot in trans[i+1: ]:
                    pass


if __name__ == "__main__":
    so = Solution()
    print(so.invalidTransactions(["alice,20,800,mtv","alice,50,100,beijing"]))
