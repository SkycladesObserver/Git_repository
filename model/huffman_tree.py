import heapq
from .binary_tree_node import BinaryTreeNode


class HuffmanTree:
    """哈夫曼树实现"""

    def __init__(self):
        self.root = None
        self.codes = {}  # 存储字符的哈夫曼编码

    def build_from_text(self, text):
        """从文本构建哈夫曼树"""
        if not text:
            return

        # 计算字符频率
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1

        # 构建哈夫曼树
        self.build_from_frequency(frequency)

    def build_from_frequency(self, frequency):
        """从频率字典构建哈夫曼树"""
        if not frequency:
            return

        # 创建优先队列（最小堆）
        heap = []
        for char, freq in frequency.items():
            node = BinaryTreeNode({'char': char, 'freq': freq, 'is_leaf': True})
            heapq.heappush(heap, (freq, id(node), node))

        # 构建哈夫曼树
        while len(heap) > 1:
            # 取出两个最小频率的节点
            freq1, _, node1 = heapq.heappop(heap)
            freq2, _, node2 = heapq.heappop(heap)

            # 创建新节点，频率为两个子节点频率之和
            merged_freq = freq1 + freq2
            merged_node = BinaryTreeNode({
                'char': None,
                'freq': merged_freq,
                'is_leaf': False
            })
            merged_node.left = node1
            merged_node.right = node2
            node1.parent = merged_node
            node2.parent = merged_node

            heapq.heappush(heap, (merged_freq, id(merged_node), merged_node))

        # 堆中最后一个节点就是根节点
        if heap:
            _, _, self.root = heapq.heappop(heap)

        # 生成哈夫曼编码
        self._generate_codes(self.root, "")

    def _generate_codes(self, node, code):
        """生成哈夫曼编码"""
        if node is None:
            return

        if node.data['is_leaf']:
            self.codes[node.data['char']] = code
            return

        self._generate_codes(node.left, code + "0")
        self._generate_codes(node.right, code + "1")

    def encode(self, text):
        """编码文本"""
        encoded = ""
        for char in text:
            if char in self.codes:
                encoded += self.codes[char]
            else:
                raise ValueError(f"字符 '{char}' 不在哈夫曼树中")
        return encoded

    def decode(self, encoded_text):
        """解码文本"""
        decoded = ""
        current = self.root

        for bit in encoded_text:
            if bit == '0':
                current = current.left
            else:
                current = current.right

            if current.data['is_leaf']:
                decoded += current.data['char']
                current = self.root

        return decoded

    def get_tree_structure(self):
        """获取树结构信息，用于可视化"""
        if self.root is None:
            return None

        def build_structure(node):
            if node is None:
                return None

            # 显示字符和频率
            if node.data['is_leaf']:
                display_text = f"'{node.data['char']}':{node.data['freq']}"
            else:
                display_text = f"{node.data['freq']}"

            return {
                'data': display_text,
                'id': str(id(node)),  # 使用节点内存地址作为唯一ID
                'is_leaf': node.data['is_leaf'],
                'left': build_structure(node.left),
                'right': build_structure(node.right)
            }

        return build_structure(self.root)

    def get_codes(self):
        """获取哈夫曼编码表"""
        return self.codes

    def clear(self):
        """清空树"""
        self.root = None
        self.codes = {}