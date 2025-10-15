class Queue:
    """顺序队列实现"""

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0  # 队头指针
        self.rear = -1  # 队尾指针
        self.count = 0  # 元素个数

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.capacity

    def enqueue(self, item):
        if self.is_full():
            raise Exception("队列已满")
        self.rear = (self.rear + 1) % self.capacity
        self.data[self.rear] = item
        self.count += 1
        return item

    def dequeue(self):
        if self.is_empty():
            raise Exception("队列为空")
        item = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self.data[self.front]

    def size(self):
        return self.count

    def get_all_data(self):
        """获取队列中的所有数据（按顺序）"""
        result = []
        if self.is_empty():
            return result

        current = self.front
        for _ in range(self.count):
            result.append(self.data[current])
            current = (current + 1) % self.capacity

        return result