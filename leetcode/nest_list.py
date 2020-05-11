# coding=utf-8
# builtins
# third party package
# self built


class NestedIterator:
    def __init__(self, nestedList):

        self.nums = nestedList
        self.has_next = True
        self.gen = self.next_num(self.nums)
        self.cur = None

    def next(self) -> int:
        if self.cur is None:
            if not self.hasNext():
                raise StopIteration
        res = self.cur
        self.cur = None
        return res

    def next_num(self, nums):
        for num in nums:
            if isinstance(num, int):
                yield num
            else:
                nest_nums = self.next_num(num)
                for n in nest_nums:
                    yield n

    def hasNext(self) -> bool:
        if self.cur is not None:
            return True
        try:
            c = next(self.gen)
            self.cur = c
            self.has_next = True
        except:
            self.has_next = False
        return self.has_next


so = NestedIterator( [[1,1],2,[1,1]])
while 1:
    print(so.next())
    print(so.hasNext())
    print(so.hasNext())