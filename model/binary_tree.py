from .binary_tree_node import BinaryTreeNode
from collections import deque
import uuid

class BinaryTree:
    """二叉树实现"""

    def __init__(self):
        self.root = None
        self.node_counter = 0  # 确保这里初始化了node_counter

    def is_empty(self):
        return self.root is None

    def insert_level_order(self, data):
        """按层次顺序插入单个节点"""
        # 为每个节点创建唯一标识符
        self.node_counter += 1
        node_data = {
            'value': data,
            'id': f"bt_{self.node_counter}"  # 唯一标识符
        }

        new_node = BinaryTreeNode(node_data)

        if self.root is None:
            self.root = new_node
            return True

        # 使用队列进行层次遍历，找到第一个可以插入的位置
        queue = [self.root]

        while queue:
            current = queue.pop(0)

            # 如果左子节点为空，插入到左子节点
            if current.left is None:
                current.left = new_node
                new_node.parent = current
                return True
            else:
                queue.append(current.left)

            # 如果右子节点为空，插入到右子节点
            if current.right is None:
                current.right = new_node
                new_node.parent = current
                return True
            else:
                queue.append(current.right)

        return False

    def _create_node(self, data):
        """创建节点"""
        node = BinaryTreeNode(data)
        return node

    def insert_level_order_batch(self, data_list):
        """批量按层次顺序插入节点"""
        if not data_list:
            return

        # 清空当前树
        self.root = None
        self.node_counter = 0

        # 批量插入
        for data in data_list:
            self.insert_level_order(data)

    def insert_left(self, parent_data, data):
        """在指定父节点的左侧插入节点"""
        parent = self._find_node(self.root, parent_data)
        if parent:
            if parent.left is None:
                parent.left = BinaryTreeNode(data)
                parent.left.parent = parent
                return True
        return False

    def insert_right(self, parent_data, data):
        """在指定父节点的右侧插入节点"""
        parent = self._find_node(self.root, parent_data)
        if parent:
            if parent.right is None:
                parent.right = BinaryTreeNode(data)
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
            result.append(current.data)

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return result

    def clear(self):
        """清空树"""
        self.root = None

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