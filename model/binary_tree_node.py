class BinaryTreeNode:
    """二叉树节点"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None  # 用于某些算法

    def __str__(self):
        return str(self.data)

    def is_leaf(self):
        """判断是否为叶子节点"""
        return self.left is None and self.right is None