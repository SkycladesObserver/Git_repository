import json
import pickle
from datetime import datetime


class DataStructureSerializer:
    """数据结构序列化工具类"""

    @staticmethod
    def serialize_linked_list(linked_list):
        """序列化链表"""
        if linked_list.head is None:
            return {"type": "LinkedList", "data": []}

        data = []
        current = linked_list.head
        while current:
            data.append(current.data)
            current = current.next

        return {"type": "LinkedList", "data": data}

    @staticmethod
    def deserialize_linked_list(data):
        """反序列化链表"""
        from model.linked_list import LinkedList

        linked_list = LinkedList()
        for item in data:
            linked_list.insert_at_end(item)

        return linked_list

    @staticmethod
    def serialize_stack(stack):
        """序列化栈"""
        return {
            "type": "Stack",
            "data": stack.get_all_data(),
            "capacity": stack.capacity
        }

    @staticmethod
    def deserialize_stack(data):
        """反序列化栈"""
        from model.stack import Stack

        stack = Stack(data.get("capacity", 10))
        # 重新构建栈
        for item in reversed(data["data"]):
            if item is not None:
                stack.push(item)

        return stack

    @staticmethod
    def serialize_queue(queue):
        """序列化队列"""
        return {
            "type": "Queue",
            "data": queue.get_all_data(),
            "capacity": queue.capacity
        }

    @staticmethod
    def deserialize_queue(data):
        """反序列化队列"""
        from model.queue import Queue

        queue = Queue(data.get("capacity", 10))
        for item in data["data"]:
            queue.enqueue(item)

        return queue

    @staticmethod
    def serialize_binary_tree(tree):
        """序列化二叉树"""

        def serialize_node(node):
            if node is None:
                return None
            return {
                "data": node.data,
                "left": serialize_node(node.left),
                "right": serialize_node(node.right)
            }

        return {
            "type": "BinaryTree",
            "data": serialize_node(tree.root)
        }

    @staticmethod
    def deserialize_binary_tree(data):
        """反序列化二叉树"""
        from model.binary_tree import BinaryTree

        def deserialize_node(node_data):
            if node_data is None:
                return None

            # 创建节点
            node = BinaryTreeNode(node_data["data"])
            node.left = deserialize_node(node_data.get("left"))
            node.right = deserialize_node(node_data.get("right"))

            return node

        tree = BinaryTree()
        tree.root = deserialize_node(data["data"])
        return tree

    @staticmethod
    def serialize_bst(bst):
        """序列化二叉搜索树"""

        def serialize_node(node):
            if node is None:
                return None
            return {
                "data": node.data,
                "left": serialize_node(node.left),
                "right": serialize_node(node.right)
            }

        return {
            "type": "BinarySearchTree",
            "data": serialize_node(bst.root)
        }

    @staticmethod
    def deserialize_bst(data):
        """反序列化二叉搜索树"""
        from model.binary_search_tree import BinarySearchTree

        def deserialize_node(node_data):
            if node_data is None:
                return None

            node = BinaryTreeNode(node_data["data"])
            node.left = deserialize_node(node_data.get("left"))
            node.right = deserialize_node(node_data.get("right"))

            return node

        bst = BinarySearchTree()
        bst.root = deserialize_node(data["data"])
        return bst

    @staticmethod
    def serialize_huffman(huffman_tree):
        """序列化哈夫曼树"""

        def serialize_node(node):
            if node is None:
                return None
            return {
                "data": node.data,
                "left": serialize_node(node.left),
                "right": serialize_node(node.right)
            }

        return {
            "type": "HuffmanTree",
            "data": serialize_node(huffman_tree.root),
            "codes": huffman_tree.get_codes()
        }

    @staticmethod
    def deserialize_huffman(data):
        """反序列化哈夫曼树"""
        from model.huffman_tree import HuffmanTree

        def deserialize_node(node_data):
            if node_data is None:
                return None

            node = BinaryTreeNode(node_data["data"])
            node.left = deserialize_node(node_data.get("left"))
            node.right = deserialize_node(node_data.get("right"))

            return node

        huffman_tree = HuffmanTree()
        huffman_tree.root = deserialize_node(data["data"])
        huffman_tree.codes = data.get("codes", {})
        return huffman_tree

    @staticmethod
    def serialize_avl(avl_tree):
        """序列化AVL树"""

        def serialize_node(node):
            if node is None:
                return None
            return {
                "data": node.data,
                "height": node.height,
                "left": serialize_node(node.left),
                "right": serialize_node(node.right)
            }

        return {
            "type": "AVLTree",
            "data": serialize_node(avl_tree.root)
        }

    @staticmethod
    def deserialize_avl(data):
        """反序列化AVL树"""
        from model.avl_tree import AVLTree, AVLNode

        def deserialize_node(node_data):
            if node_data is None:
                return None

            node = AVLNode(node_data["data"])
            node.height = node_data.get("height", 1)
            node.left = deserialize_node(node_data.get("left"))
            node.right = deserialize_node(node_data.get("right"))

            if node.left:
                node.left.parent = node
            if node.right:
                node.right.parent = node

            return node

        avl_tree = AVLTree()
        avl_tree.root = deserialize_node(data["data"])
        return avl_tree

    @staticmethod
    def save_to_file(data, filename):
        """保存数据到文件"""
        # 添加元数据
        save_data = {
            "metadata": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "data_structure": data.get("type", "Unknown")
            },
            "data": data
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_from_file(filename):
        """从文件加载数据"""
        with open(filename, 'r', encoding='utf-8') as f:
            save_data = json.load(f)

        return save_data["data"]