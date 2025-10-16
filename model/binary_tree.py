from .binary_tree_node import BinaryTreeNode
from collections import deque


class BinaryTree:
    """二叉树实现"""

    def __init__(self):
        self.root = None
        self.node_count = 0  # 节点计数器，用于处理重复值

    def is_empty(self):
        return self.root is None

    def insert_level_order(self, data_list):
        """按层次顺序插入节点"""
        if not data_list:
            return

        # 为每个数据创建唯一标识
        unique_data_list = []
        for data in data_list:
            unique_data = f"{data}_{self.node_count}"
            unique_data_list.append(unique_data)
            self.node_count += 1

        self.root = BinaryTreeNode(unique_data_list[0])
        queue = deque([self.root])
        i = 1

        while i < len(unique_data_list):
            current = queue.popleft()

            # 插入左子节点
            if unique_data_list[i] is not None:
                current.left = BinaryTreeNode(unique_data_list[i])
                current.left.parent = current
                queue.append(current.left)
            i += 1

            if i >= len(unique_data_list):
                break

            # 插入右子节点
            if unique_data_list[i] is not None:
                current.right = BinaryTreeNode(unique_data_list[i])
                current.right.parent = current
                queue.append(current.right)
            i += 1

    def insert_left(self, parent_data, data):
        """在指定父节点的左侧插入节点"""
        parent = self._find_node(self.root, parent_data)
        if parent:
            unique_data = f"{data}_{self.node_count}"
            self.node_count += 1
            parent.left = BinaryTreeNode(unique_data)
            parent.left.parent = parent
            return True
        return False

    def insert_right(self, parent_data, data):
        """在指定父节点的右侧插入节点"""
        parent = self._find_node(self.root, parent_data)
        if parent:
            unique_data = f"{data}_{self.node_count}"
            self.node_count += 1
            parent.right = BinaryTreeNode(unique_data)
            parent.right.parent = parent
            return True
        return False

    def _find_node(self, node, data):
        """查找包含指定数据的节点"""
        if node is None:
            return None

        if node.data == data:
            return node

        left_result = self._find_node(node.left, data)
        if left_result:
            return left_result

        return self._find_node(node.right, data)

    def get_level_order(self):
        """获取层次遍历结果"""
        if self.root is None:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            current = queue.popleft()
            # 提取原始数据（去掉计数器部分）
            original_data = current.data.split('_')[0]
            result.append(int(original_data))

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return result

    def clear(self):
        """清空树"""
        self.root = None
        self.node_count = 0

    def get_tree_structure(self):
        """获取树结构信息，用于可视化"""
        if self.root is None:
            return None

        def build_structure(node):
            if node is None:
                return None

            # 提取原始数据（去掉计数器部分）
            original_data = node.data.split('_')[0]

            return {
                'data': original_data,
                'left': build_structure(node.left),
                'right': build_structure(node.right)
            }

        return build_structure(self.root)