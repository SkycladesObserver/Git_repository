from .avl_node import AVLNode


class AVLTree:
    """AVL树（平衡二叉搜索树）实现"""

    def __init__(self):
        self.root = None
        self.node_counter = 0

    def is_empty(self):
        return self.root is None

    def get_height(self, node):
        """获取节点高度"""
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        """获取节点的平衡因子"""
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        """更新节点高度"""
        if node is not None:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_right(self, y):
        """右旋转"""
        x = y.left
        T2 = x.right

        # 执行旋转
        x.right = y
        y.left = T2

        # 更新父指针
        if T2 is not None:
            T2.parent = y
        x.parent = y.parent
        y.parent = x

        # 更新高度
        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        """左旋转"""
        y = x.right
        T2 = y.left

        # 执行旋转
        y.left = x
        x.right = T2

        # 更新父指针
        if T2 is not None:
            T2.parent = x
        y.parent = x.parent
        x.parent = y

        # 更新高度
        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, data):
        """插入节点"""
        self.node_counter += 1
        node_data = {
            'value': data,
            'id': f"avl_{self.node_counter}",  # 唯一标识符
            'balance': 0  # 平衡因子
        }

        self.root = self._insert_recursive(self.root, node_data)
        return True

    def _insert_recursive(self, node, data):
        """递归插入辅助方法"""
        # 1. 执行正常的BST插入
        if node is None:
            return AVLNode(data)

        if data['value'] < node.data['value']:
            node.left = self._insert_recursive(node.left, data)
            node.left.parent = node
        elif data['value'] > node.data['value']:
            node.right = self._insert_recursive(node.right, data)
            node.right.parent = node
        else:
            # 重复值，插入到右子树（AVL允许重复值）
            node.right = self._insert_recursive(node.right, data)
            node.right.parent = node

        # 2. 更新节点高度
        self.update_height(node)

        # 3. 获取平衡因子
        balance = self.get_balance(node)
        node.data['balance'] = balance  # 存储平衡因子用于显示

        # 4. 如果不平衡，则有4种情况

        # 左左情况（右旋转）
        if balance > 1 and data['value'] < node.left.data['value']:
            return self.rotate_right(node)

        # 右右情况（左旋转）
        if balance < -1 and data['value'] > node.right.data['value']:
            return self.rotate_left(node)

        # 左右情况（先左旋后右旋）
        if balance > 1 and data['value'] > node.left.data['value']:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # 右左情况（先右旋后左旋）
        if balance < -1 and data['value'] < node.right.data['value']:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

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
        # 1. 执行标准的BST删除
        if node is None:
            return node

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
                temp = self._find_min(node.right)
                node.data = temp.data
                node.right = self._delete_recursive(node.right, temp.data['value'])

        # 如果树只有一个节点，直接返回
        if node is None:
            return node

        # 2. 更新节点高度
        self.update_height(node)

        # 3. 获取平衡因子
        balance = self.get_balance(node)
        node.data['balance'] = balance

        # 4. 如果不平衡，则有4种情况

        # 左左情况
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # 左右情况
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # 右右情况
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # 右左情况
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

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
                'data': f"{node.data['value']}({node.data['balance']})",  # 显示值和平衡因子
                'id': node.data['id'],
                'balance': node.data['balance'],
                'left': build_structure(node.left),
                'right': build_structure(node.right)
            }

        return build_structure(self.root)

    def clear(self):
        """清空树"""
        self.root = None
        self.node_counter = 0