# coding=utf-8
# builtins
# third party package
# self built
# Definition for singly-linked list.


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    @classmethod
    def get_node_from_list(cls, l: list):
        ret = cls(0)
        node = None
        for i in l:
            if not node:
                node = cls(i)
                ret = node
            else:
                node.next = cls(i)
                node = node.next
        return ret

    def to_list(self):
        l = list()
        node = self
        while node is not None:
            l.append(node.val)
            node = node.next

        return l


class Solution:
    def partition(self, head: ListNode, x: int) -> ListNode:
        if not head.next:
            return head
        node_s = None
        ret_s = None
        node_l = None
        ret_l = None
        node = head
        while node:
            print(node.val, end='    ')
            if node.val < x:
                if not node_s:
                    node_s = ListNode(node.val)
                    ret_s = node_s
                else:
                    node_s.next = ListNode(node.val)
                    node_s = node_s.next
            else :
                if not node_l:
                    node_l = ListNode(node.val)
                    ret_l = node_l
                else:
                    node_l.next = ListNode(node.val)
                    node_l = node_l.next

            node = node.next
        if ret_s:
            node_s.next = ret_l
            return ret_s
        else:
            return node_l


so = Solution()
max()
# print(ListNode.get_node_from_list([1, 4, 3, 2, 5, 2]))
# print(so.partition(ListNode.get_node_from_list([1, 4, 3, 2, 5, 2]), 3).to_list())
print(so.partition(ListNode.get_node_from_list([1, 1]), 0).to_list())