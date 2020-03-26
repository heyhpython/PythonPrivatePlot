from typing import List


class Solution:
    def filterRestaurants(self, restaurants: List[List[int]],
                          veganFriendly: int,
                          maxPrice: int,
                          maxDistance: int) -> List[int]:
        # 1.过滤素食、价格和距离
        restaurants = filter(
            lambda r: r[2] >= veganFriendly and
            r[3] <= maxPrice and
            r[4] <= maxDistance, restaurants)
        # 2.按照评分和id排序返回id
        return [i[0] for i in sorted(restaurants, key=lambda r: (-r[1], -r[0]))]


if __name__ == "__main__":
    so = Solution()
    restaurants = [
        [1, 4, 1, 40, 10],
        [2, 8, 0, 50, 5],
        [3, 8, 1, 30, 4],
        [4, 10, 0, 10, 3],
        [5, 1, 1, 15, 1]]
    veganFriendly = 0
    maxPrice = 50
    maxDistance = 10
    print(so.filterRestaurants(restaurants, 0, 50, 10))
    print(so.filterRestaurants(restaurants, 0, 30, 3))
