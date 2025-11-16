from .binary_tree_node import BinaryTreeNode


class AVLNode(BinaryTreeNode):
    """AVL树节点，扩展二叉树节点"""

    def __init__(self, data):
        super().__init__(data)
        self.height = 1  # 节点高度，用于平衡因子计算