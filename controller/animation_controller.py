from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import time


class AnimationController(QObject):
    """动画控制器"""

    # 信号：更新状态、步骤变化、完成
    status_changed = pyqtSignal(str)
    step_changed = pyqtSignal(int, str)
    animation_finished = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_demo = None
        self.steps = []
        self.current_step = 0
        self.is_playing = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.animation_speed = 1000  # 默认速度：1秒/步

    def set_animation_speed(self, speed):
        """设置动画速度（毫秒）"""
        self.animation_speed = speed
        if self.timer.isActive():
            self.timer.setInterval(speed)

    def load_demo(self, demo_name):
        """加载演示"""
        self.current_demo = demo_name
        self.steps = self._generate_demo_steps(demo_name)
        self.current_step = 0
        self.status_changed.emit(f"已加载演示: {demo_name}")
        return len(self.steps)

    def play(self):
        """开始播放"""
        if not self.steps:
            QMessageBox.warning(self.main_window, "警告", "请先选择演示内容")
            return

        self.is_playing = True
        self.timer.start(self.animation_speed)
        self.status_changed.emit("动画演示开始")

    def pause(self):
        """暂停"""
        self.is_playing = False
        self.timer.stop()
        self.status_changed.emit("动画演示暂停")

    def stop(self):
        """停止"""
        self.is_playing = False
        self.timer.stop()
        self.current_step = 0
        self.status_changed.emit("动画演示停止")
        self.animation_finished.emit()

    def next_step(self):
        """执行下一步"""
        if self.current_step >= len(self.steps):
            self.stop()
            return

        step = self.steps[self.current_step]
        self._execute_step(step)
        self.step_changed.emit(self.current_step + 1, step.get('description', ''))
        self.current_step += 1

        if self.current_step >= len(self.steps):
            self.stop()

    def previous_step(self):
        """执行上一步"""
        if self.current_step > 0:
            self.current_step -= 1
            # 重新执行到当前步骤的所有操作
            self._reset_to_initial()
            for i in range(self.current_step):
                step = self.steps[i]
                self._execute_step(step)

            step = self.steps[self.current_step]
            self.step_changed.emit(self.current_step + 1, step.get('description', ''))

    def _execute_step(self, step):
        """执行单个步骤"""
        action = step.get('action')
        data = step.get('data', {})

        try:
            if action == 'insert_beginning':
                self.main_window.linked_list.insert_at_beginning(data['value'])
            elif action == 'insert_end':
                self.main_window.linked_list.insert_at_end(data['value'])
            elif action == 'delete_position':
                self.main_window.linked_list.delete_at_position(data['position'])
            elif action == 'push':
                self.main_window.stack.push(data['value'])
            elif action == 'pop':
                self.main_window.stack.pop()
            elif action == 'enqueue':
                self.main_window.queue.enqueue(data['value'])
            elif action == 'dequeue':
                self.main_window.queue.dequeue()
            elif action == 'bst_insert':
                self.main_window.bst.insert(data['value'])
            elif action == 'bst_delete':
                self.main_window.bst.delete(data['value'])
            elif action == 'avl_insert':
                self.main_window.avl_tree.insert(data['value'])
            elif action == 'huffman_build':
                self.main_window.huffman_tree.build_from_text(data['text'])
            # 添加更多操作...

            # 更新显示
            self.main_window.update_display(step.get('description', ''))

        except Exception as e:
            self.status_changed.emit(f"执行错误: {str(e)}")

    def _reset_to_initial(self):
        """重置到初始状态"""
        # 根据当前演示类型重置数据结构
        if self.current_demo and '链表' in self.current_demo:
            self.main_window.linked_list.clear()
        elif self.current_demo and '栈' in self.current_demo:
            self.main_window.stack = self.main_window.stack.__class__(10)
        elif self.current_demo and '队列' in self.current_demo:
            self.main_window.queue = self.main_window.queue.__class__(10)
        elif self.current_demo and '二叉搜索树' in self.current_demo:
            self.main_window.bst.clear()
        elif self.current_demo and 'AVL树' in self.current_demo:
            self.main_window.avl_tree.clear()
        elif self.current_demo and '哈夫曼树' in self.current_demo:
            self.main_window.huffman_tree.clear()

    def _generate_demo_steps(self, demo_name):
        """生成演示步骤"""
        steps = []

        if demo_name == "链表基本操作":
            steps = [
                {'action': 'insert_beginning', 'data': {'value': 10}, 'description': '在链表开头插入 10'},
                {'action': 'insert_beginning', 'data': {'value': 20}, 'description': '在链表开头插入 20'},
                {'action': 'insert_end', 'data': {'value': 30}, 'description': '在链表末尾插入 30'},
                {'action': 'insert_end', 'data': {'value': 40}, 'description': '在链表末尾插入 40'},
                {'action': 'delete_position', 'data': {'position': 1}, 'description': '删除位置 1 的节点'},
            ]

        elif demo_name == "栈的LIFO特性":
            steps = [
                {'action': 'push', 'data': {'value': 10}, 'description': '压入 10'},
                {'action': 'push', 'data': {'value': 20}, 'description': '压入 20'},
                {'action': 'push', 'data': {'value': 30}, 'description': '压入 30'},
                {'action': 'pop', 'data': {}, 'description': '弹出栈顶元素'},
                {'action': 'pop', 'data': {}, 'description': '弹出栈顶元素'},
            ]

        elif demo_name == "队列的FIFO特性":
            steps = [
                {'action': 'enqueue', 'data': {'value': 10}, 'description': '入队 10'},
                {'action': 'enqueue', 'data': {'value': 20}, 'description': '入队 20'},
                {'action': 'enqueue', 'data': {'value': 30}, 'description': '入队 30'},
                {'action': 'dequeue', 'data': {}, 'description': '出队元素'},
                {'action': 'dequeue', 'data': {}, 'description': '出队元素'},
            ]

        elif demo_name == "二叉搜索树构建":
            steps = [
                {'action': 'bst_insert', 'data': {'value': 50}, 'description': '插入根节点 50'},
                {'action': 'bst_insert', 'data': {'value': 30}, 'description': '插入左子节点 30'},
                {'action': 'bst_insert', 'data': {'value': 70}, 'description': '插入右子节点 70'},
                {'action': 'bst_insert', 'data': {'value': 20}, 'description': '插入 20'},
                {'action': 'bst_insert', 'data': {'value': 40}, 'description': '插入 40'},
                {'action': 'bst_insert', 'data': {'value': 60}, 'description': '插入 60'},
                {'action': 'bst_insert', 'data': {'value': 80}, 'description': '插入 80'},
            ]

        elif demo_name == "AVL树平衡演示":
            steps = [
                {'action': 'avl_insert', 'data': {'value': 10}, 'description': '插入 10'},
                {'action': 'avl_insert', 'data': {'value': 20}, 'description': '插入 20（右旋转）'},
                {'action': 'avl_insert', 'data': {'value': 5}, 'description': '插入 5'},
                {'action': 'avl_insert', 'data': {'value': 15}, 'description': '插入 15'},
                {'action': 'avl_insert', 'data': {'value': 25}, 'description': '插入 25（左旋转）'},
            ]

        elif demo_name == "哈夫曼编码":
            steps = [
                {'action': 'huffman_build', 'data': {'text': 'ABRACADABRA'},
                 'description': '构建哈夫曼树: ABRACADABRA'},
            ]

        return steps