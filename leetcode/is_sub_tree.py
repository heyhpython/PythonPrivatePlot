# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSubtree(self, s: TreeNode, t: TreeNode) -> bool:
        if s is None:
            return False
        if s.val == t.val and self.is_equal(s, t):
            return True
        return self.isSubtree(s.left, t) or self.isSubtree(s.right, t)

    def is_equal(self, t1: TreeNode, t2: TreeNode) -> bool:
        if not(t1 or t2):
            return True
        elif not (t1 and t2):
            return False
        return t1.val == t2.val \
            and self.is_equal(t1.left, t2.left)\
            and self.is_equal(t1.right, t2.right)
