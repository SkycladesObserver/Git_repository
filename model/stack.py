class Stack:
    """顺序栈实现"""

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1  # 栈顶指针

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == self.capacity - 1

    def push(self, item):
        if self.is_full():
            raise Exception("栈已满")
        self.top += 1
        self.data[self.top] = item
        return item

    def pop(self):
        if self.is_empty():
            raise Exception("栈为空")
        item = self.data[self.top]
        self.data[self.top] = None
        self.top -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self.data[self.top]

    def size(self):
        return self.top + 1

    def get_all_data(self):
        return self.data[:self.top + 1]