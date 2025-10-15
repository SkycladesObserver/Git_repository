from .node import Node


class LinkedList:
    """链表数据结构"""

    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        """在链表开头插入节点"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return new_node

    def insert_at_end(self, data):
        """在链表末尾插入节点"""
        new_node = Node(data)

        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.size += 1
        return new_node

    def insert_at_position(self, position, data):
        """在指定位置插入节点"""
        if position < 0 or position > self.size:
            raise IndexError("位置超出范围")

        if position == 0:
            return self.insert_at_beginning(data)

        new_node = Node(data)
        current = self.head

        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return new_node

    def delete_at_position(self, position):
        """删除指定位置的节点"""
        if position < 0 or position >= self.size:
            raise IndexError("位置超出范围")

        if position == 0:
            deleted_node = self.head
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            deleted_node = current.next
            current.next = current.next.next

        self.size -= 1
        return deleted_node

    def to_list(self):
        """将链表转换为Python列表"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        """清空链表"""
        self.head = None
        self.size = 0