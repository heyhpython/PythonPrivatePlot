# coding=utf-8
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        p, q = (p, q) if p.val < q.val else (q, p)
        p_v = p.val
        q_v = q.val
        root_v = root.val
        if p_v == root_v:
            return p_v
        elif q_v == root_v:
            return q_v
        if root_v in range(p_v+1, q_v):
            return root

        else:
            root = root.left if root_v > p_v else root.right
            if root.val == q_v:
                return q
            elif root.val == p_v:
                return p
            else:
                return self.lowestCommonAncestor(root, p, q)
