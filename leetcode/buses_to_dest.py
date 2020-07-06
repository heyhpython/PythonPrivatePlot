# coding=utf-8
# builtins
from collections import defaultdict, deque
from typing import List


# third party package
# self built


class Solution:
    def numBusesToDestination(self, routes: List[List[int]], S: int, T: int) -> int:
        if S == T:
            return 0
        # 记录所有站点对应的车次
        route_dict = defaultdict(set)
        for bus, route in enumerate(routes):
            for sta in route:
                route_dict[sta].add(bus)

        # 访问标记 访问过的车次 不再访问
        vis = [False for _ in range(len(routes))]

        deq = deque()
        deq.append((S, 1))
        while deq:
            cur_sta, res = deq.pop()
            for bus in route_dict[cur_sta]:
                if vis[bus]:
                    continue
                for s in routes[bus]:
                    if s == T:
                        return res
                    # 深度优先
                    deq.appendleft((s, res + 1))
                vis[bus] = True
        return -1


so = Solution()
print(so.numBusesToDestination([[1, 2, 7], [3, 6, 7]], 1, 6))
