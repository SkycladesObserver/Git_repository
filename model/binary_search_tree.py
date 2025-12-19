from .binary_tree_node import BinaryTreeNode
import uuid

class BinarySearchTree:
    """二叉搜索树实现"""

    def __init__(self):
        self.root = None
        self.node_counter = 0  # 节点计数器，用于生成唯一ID

    def insert(self, data):
        """插入节点"""
        # 为每个节点创建唯一标识符
        self.node_counter += 1
        node_data = {
            'value': data,
            'id': f"bst_{self.node_counter}"  # 唯一标识符
        }

        print(f"插入节点: {data}, ID: bst_{self.node_counter}")  # 调试输出

        if self.root is None:
            self.root = BinaryTreeNode(node_data)
            return True
        else:
            return self._insert_recursive(self.root, node_data)

    def _insert_recursive(self, node, data):
        """递归插入辅助方法"""
        if data['value'] < node.data['value']:
            if node.left is None:
                node.left = BinaryTreeNode(data)
                node.left.parent = node
                return True
            else:
                return self._insert_recursive(node.left, data)
        else:  # 允许重复值，插入到右子树
            if node.right is None:
                node.right = BinaryTreeNode(data)
                node.right.parent = node
                return True
            else:
                return self._insert_recursive(node.right, data)

    def search(self, data):
        """搜索节点"""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        """递归搜索辅助方法"""
        if node is None:
            return None

        if data == node.data['value']:
            return node
        elif data < node.data['value']:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def delete(self, data):
        """删除节点"""
        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, node, data):
        """递归删除辅助方法"""
        if node is None:
            return None

        if data < node.data['value']:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data['value']:
            node.right = self._delete_recursive(node.right, data)
        else:
            # 找到要删除的节点
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # 有两个子节点，找到右子树的最小节点
                min_node = self._find_min(node.right)
                node.data = min_node.data
                node.right = self._delete_recursive(node.right, min_node.data['value'])

        return node

    def _find_min(self, node):
        """找到子树中的最小节点"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_tree_structure(self):
        """获取树结构信息，用于可视化"""
        if self.root is None:
            return None

        def build_structure(node):
            if node is None:
                return None

            return {
                'data': node.data['value'],  # 只显示值
                'id': node.data['id'],  # 唯一标识符
                'left': build_structure(node.left),
                'right': build_structure(node.right)
            }

        return build_structure(self.root)

    def clear(self):
        """清空树"""
        self.root = None
        self.node_counter = 0