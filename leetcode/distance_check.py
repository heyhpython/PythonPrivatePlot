# coding=utf-8
# builtins
from typing import List, Set
# third party package
# self built
from .tree import Tree


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, K: int) -> List[int]:
        def dfs(node, p=None):
            if node:
                node.par = p
                dfs(node.left, node)
                dfs(node.right, node)
        dfs(root)

        queue = [(target, 0)]
        checked = set((target.val))

        while queue:
            if queue[0][1] == K:
                return [node.val for node, d in queue]
            node, d = queue.pop(0)
            for nei in (node.left, node.right, node.par):
                if nei and nei.val not in checked:
                    checked.add(nei.val)
                    queue.append((nei, d+1))
        return []

    def find_target_in_deep(self, root: TreeNode, target: TreeNode, stack: List):
        if root.val == target.val:
            stack.append(root)
            return True

        elif self.find_target_in_deep(root.left, target, stack) or \
            self.find_target_in_deep(root.right, target, stack):
            stack.append(root)
            return True

    def find_in_son(self, node: TreeNode, d: int, ret):
        # 查找某一节点的子节点中距离该节点为d的数
        if node is None:
            return
        if d == 0:
            ret.add(node.val)
            return
        self.find_in_son(node.left, d-1, ret)
        self.find_in_son(node.right, d-1, ret)

    def solve(self, root: TreeNode, target: TreeNode, K: int) -> List[int]:

        def dfs(node, par=None):
            # 给节点加父节点的引用
            if node:
                node.par = par
                dfs(node.left, node)
                dfs(node.right, node)
        dfs(root)
        queue = [(target, 0)]
        checked = set()
        set.add(target.val)

        while queue:
            if queue[0][1] == K:
                return [node.val for node, _ in queue]
            node, d = queue.pop(0)
            for nei in (node.par, node.left, node.right):
                if nei and nei.val not in checked:
                    queue.append((nei, d + 1))


if __name__ == "__main__":
    so = Solution()
    tree = Tree()
    tree.construct_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    # so.distanceK(tree.root, )