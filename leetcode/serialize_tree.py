class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:

    def serialize(self, root:TreeNode):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        # return root
        queue = []
        res = []
        queue.append(root)
        import json
        while queue:
            root = queue.pop(0)
            if root is not None:
                res.append(root.val)
                queue.append(root.left)
                queue.append(root.right)
            else:
                res.append(None)
        return json.dumps(res)

        
    def deserialize(self, data: str):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        import json
        data = json.loads(data)
        if not data[0]:
            return None
        queue = []
        root = TreeNode(data[0])
        queue.append(root)
        i = 1
        while queue:
            cur = queue.pop(0)
            if cur == None:
                continue
            cur.left = TreeNode(data[i]) if data[i] else None
            cur.right = TreeNode(data[i+1]) if data[i+1] else None
            i += 2
            queue.append(cur.left)
            queue.append(cur.right)
        return root
if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    so =Codec()
    ser = so.serialize(root)
    print(ser)
    des = so.deserialize(ser)
    print(so.serialize(des))