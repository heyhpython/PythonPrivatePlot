# coding=utf-8
# builtins
# third party package
# self built

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        temp = self.next
        res = f"{self.val}"
        while temp:
            res += f"=>{temp.val}"
            temp = temp.next
        return res


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if head is None or head.next is None:
            return head
        self.r_head = ListNode(0)
        # t = [1, 2, 3, 4, 5]

        def reverse(behind: ListNode, node_left: ListNode, ) -> ListNode:
            if node_left.next is None:
                self.r_head = node_left
                node_left.next = behind
                # return node_left
            else:

                reverse(node_left, node_left.next)
                node_left.next = behind
        reverse(None, head)
        return self.r_head




t = [1, 2, 3, 4, 5]
head = ListNode(t[0])
temp = head
for i in t[1:]:
    c = ListNode(i)
    temp.next = c
    temp = c
print(head)
so = Solution()
print(so.reverseList(head))