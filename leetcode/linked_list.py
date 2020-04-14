from typing import List


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def __str__(self):
        return f"{self.val}->"


class MyLinkedList:

    def __init__(self, data: List[int] = []):
        """
        Initialize your data structure here.
        """
        self.head = Node(data[0]) if data else None
        self.tail = self.head
        self.data = data
        cur = self.head
        for num in data[1:]:
            temp = Node(num)
            temp.prev = cur
            cur.next = temp
            cur = temp
            self.tail = temp

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list.
        If the index is invalid, return -1.
        """
        n = self.get_node_with_index(index)
        return n.val if n else -1

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list.
        After the insertion,
        the new node will be the first node of the linked list.
        """
        self.data.insert(0, val)
        new_head = Node(val)
        if self.head:
            new_head.next = self.head
            self.head.prev = new_head
            self.head = new_head
        else:
            self.head = self.tail = new_head

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        self.data.append(val)
        new_tail = Node(val)
        if self.tail:
            self.tail.next = new_tail
            new_tail.prev = self.tail
            self.tail = new_tail
        else:
            # 无链表无节点
            self.head = self.tail = new_tail

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list.
        If index equals to the length of linked list,
        the node will be appended to the end of linked list.
        If index is greater than the length, the node will not be inserted.
        """
        if index > len(self.data):
            print("index > length")
            return
        elif index == len(self.data):
            print("add at tail")
            return self.addAtTail(val)
        pos = self.get_node_with_index(index)
        print(pos)
        if pos:
            # 第index位
            self.data.insert(index, val)
            temp = Node(val)
            temp.prev = pos.prev
            pos.prev.next = temp
            temp.next = pos
            pos.prev = temp

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        pos = self.get_node_with_index(index)
        print(pos)
        if pos:
            # 第index位
            self.data.pop(index)
            if pos.prev and pos.next:
                pos.prev.next = pos.next
                pos.next.prev = pos.prev

            elif pos.prev and not pos.next:
                # delete tail
                pos.prev.next = None
                self.tail = pos.next
            elif not pos.prev and pos.next:
                # delete head
                print("DELETE HEAD")
                self.head = pos.next
                pos.next.prev = None
            elif not pos.prev and not pos.next:
                self.head = self.tail = None
            del pos

    def get_node_with_index(self, index: int) -> Node:
        if index >= len(self.data):
            return
        i = 0
        res = None
        while i <= index:
            i += 1
            if not res:
                res = self.head
            else:
                res = res.next
        else:
            return res

    def __str__(self):
        s = f"data:{self.data};"
        cur = self.head
        while cur:
            s += f"{cur.val}->"
            cur = cur.next
        return s


# Your MyLinkedList object will be instantiated and called as such:
if __name__ == "__main__":
    methods = ["MyLinkedList", "addAtHead", "addAtHead", "addAtHead", "addAtIndex",
               "deleteAtIndex", "addAtHead", "addAtTail", "get", "addAtHead", "addAtIndex", "addAtHead"]
    args = [[], [7], [2], [1], [3, 0], [2], [6], [4], [4], [4], [5, 0], [6]]
    obj = MyLinkedList([args[0]])
    for i in range(1, len(methods)):
        print("++" * 20)
        method = methods[i]
        arg = args[i]
        getattr(obj, method)(*arg)
        print(f"after call method:{method}, obj:{obj} ")
