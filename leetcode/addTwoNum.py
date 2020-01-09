# coding=utf-8
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def addTwoNumbers(l1: ListNode, l2: ListNode):
    res = None
    start = None
    addition = 0
    while not (l1 is None and l2 is None):
        num1 = l1.val if l1 else 0
        num2 = l2.val if l1 else 0
        s = num1 + num2 + addition
        addition = s // 10
        if res:
            res.next = ListNode(s % 10)
            res = res.next
        else:
            start = ListNode(s % 10)
            res = start
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    if addition != 0:
        res.next = ListNode(addition)
    return start


l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)
l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)
print(addTwoNumbers(l1, l2))
