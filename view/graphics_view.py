
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPolygonF
from PyQt5.QtCore import QRectF


class NodeGraphicsItem:
    """图形节点项"""

    def __init__(self, data, x, y, width=60, height=40):
        self.data = data
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._opacity = 1.0

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value

    def get_center(self):
        """获取节点中心位置"""
        return QPointF(self.x + self.width / 2, self.y + self.height / 2)


class GraphicsView(QGraphicsView):
    """自定义图形视图，用于绘制数据结构"""

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 设置抗锯齿和其他渲染提示
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)

        self.setSceneRect(0, 0, 800, 400)

        # 存储图形项
        self.node_items = []
        self.animation_timeline = []
        self.current_animation_index = 0

        # 设置背景
        self.setStyleSheet("background-color: #f5f5f5; border: 1px solid #cccccc;")

    def draw_linked_list(self, linked_list):
        """绘制链表"""
        self.clear_scene()
        self.node_items = []

        nodes = []
        current = linked_list.head
        while current:
            nodes.append(current.data)
            current = current.next

        # 计算布局
        node_width = 80
        node_height = 50
        horizontal_spacing = 100
        start_x = 50
        start_y = 200

        # 绘制节点和连线
        for i, data in enumerate(nodes):
            x = start_x + i * (node_width + horizontal_spacing)
            y = start_y

            # 创建图形节点
            node_item = NodeGraphicsItem(data, x, y, node_width, node_height)
            self.node_items.append(node_item)

            # 绘制节点矩形
            rect = self.scene.addRect(x, y, node_width, node_height)
            rect.setBrush(QBrush(QColor(173, 216, 230)))  # 浅蓝色
            rect.setPen(QPen(Qt.black, 2))

            # 绘制节点数据
            text = self.scene.addText(str(data))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 12, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x + node_width / 2 - text_rect.width() / 2,
                        y + node_height / 2 - text_rect.height() / 2)

            # 如果不是最后一个节点，绘制箭头
            if i < len(nodes) - 1:
                next_x = x + node_width + horizontal_spacing
                self._draw_arrow(x + node_width, y + node_height / 2,
                                 next_x, y + node_height / 2)

    def _draw_arrow(self, start_x, start_y, end_x, end_y):
        """绘制箭头"""
        # 绘制直线
        line = self.scene.addLine(start_x, start_y, end_x, end_y)
        line.setPen(QPen(Qt.black, 2))

        # 绘制箭头头部
        arrow_size = 10
        # 简化箭头绘制
        arrow_line1 = self.scene.addLine(end_x, end_y, end_x - arrow_size, end_y - arrow_size)
        arrow_line2 = self.scene.addLine(end_x, end_y, end_x - arrow_size, end_y + arrow_size)
        arrow_line1.setPen(QPen(Qt.black, 2))
        arrow_line2.setPen(QPen(Qt.black, 2))

    def highlight_node(self, position, color=QColor(255, 255, 0)):
        """高亮指定位置的节点"""
        if 0 <= position < len(self.node_items):
            # 在实际实现中，这里应该创建高亮动画
            # 简化版本：直接改变节点颜色
            pass

    def clear_scene(self):
        """清空场景"""
        self.scene.clear()
        self.node_items = []

    def add_operation_text(self, text):
        """添加操作说明文本"""
        text_item = self.scene.addText(text)
        text_item.setDefaultTextColor(Qt.blue)
        text_item.setFont(QFont("Arial", 14))
        text_item.setPos(50, 50)

    def draw_stack(self, stack):
        """绘制栈"""
        self.clear_scene()

        # 栈的绘制参数
        start_x = 400
        start_y = 100
        element_width = 80
        element_height = 40
        spacing = 5

        # 绘制栈框架
        frame_height = stack.capacity * (element_height + spacing)
        frame = self.scene.addRect(start_x - 10, start_y - 10,
                                   element_width + 20, frame_height + 20)
        frame.setPen(QPen(Qt.black, 2))

        # 绘制栈元素（从底部到顶部）
        for i in range(stack.capacity):
            x = start_x
            y = start_y + (stack.capacity - 1 - i) * (element_height + spacing)

            # 绘制栈元素背景
            rect = self.scene.addRect(x, y, element_width, element_height)

            if i <= stack.top:
                # 有数据的元素
                rect.setBrush(QBrush(QColor(144, 238, 144)))  # 浅绿色
                rect.setPen(QPen(Qt.black, 2))

                # 绘制数据
                text = self.scene.addText(str(stack.data[i]))
                text.setDefaultTextColor(Qt.black)
                text.setFont(QFont("Arial", 12, QFont.Bold))
                text_rect = text.boundingRect()
                text.setPos(x + element_width / 2 - text_rect.width() / 2,
                            y + element_height / 2 - text_rect.height() / 2)
            else:
                # 空元素
                rect.setBrush(QBrush(QColor(240, 240, 240)))  # 浅灰色
                rect.setPen(QPen(Qt.gray, 1))

        # 绘制栈顶指针
        if stack.top >= 0:
            pointer_y = start_y + (stack.capacity - 1 - stack.top) * (element_height + spacing)
            self._draw_stack_pointer(start_x + element_width + 20, pointer_y + element_height / 2)

        # 添加标签
        top_label = self.scene.addText("栈顶")
        top_label.setPos(start_x + element_width + 50, start_y - 30)
        top_label.setDefaultTextColor(Qt.blue)

    def _draw_stack_pointer(self, x, y):
        """绘制栈顶指针"""
        # 绘制指针线
        line = self.scene.addLine(x, y, x + 40, y)
        line.setPen(QPen(Qt.red, 3))

        # 绘制箭头
        arrow = self.scene.addPolygon(
            QPolygonF([QPointF(x + 40, y),
                       QPointF(x + 30, y - 5),
                       QPointF(x + 30, y + 5)]))
        arrow.setBrush(QBrush(Qt.red))

    def draw_queue(self, queue):
        """绘制队列"""
        self.clear_scene()

        # 队列的绘制参数
        start_x = 100
        start_y = 200
        element_width = 80
        element_height = 50
        spacing = 5

        # 获取队列数据
        queue_data = queue.get_all_data()

        # 绘制队列框架
        frame_width = len(queue_data) * (element_width + spacing) if queue_data else element_width
        frame = self.scene.addRect(start_x - 10, start_y - 10,
                                   frame_width + 20, element_height + 20)
        frame.setPen(QPen(Qt.black, 2))

        # 绘制队列元素
        for i, data in enumerate(queue_data):
            x = start_x + i * (element_width + spacing)
            y = start_y

            # 绘制队列元素背景
            rect = self.scene.addRect(x, y, element_width, element_height)
            rect.setBrush(QBrush(QColor(255, 218, 185)))  # 桃色
            rect.setPen(QPen(Qt.black, 2))

            # 绘制数据
            text = self.scene.addText(str(data))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 12, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x + element_width / 2 - text_rect.width() / 2,
                        y + element_height / 2 - text_rect.height() / 2)

        # 绘制指针
        if not queue.is_empty():
            # 队头指针
            front_x = start_x - 30
            front_y = start_y + element_height / 2
            self._draw_queue_pointer(front_x, front_y, "队头")

            # 队尾指针
            rear_x = start_x + len(queue_data) * (element_width + spacing) + 10
            rear_y = start_y + element_height / 2
            self._draw_queue_pointer(rear_x, rear_y, "队尾")

        # 添加标签
        if queue.is_empty():
            empty_label = self.scene.addText("队列为空")
            empty_label.setDefaultTextColor(Qt.red)
            empty_label.setFont(QFont("Arial", 14, QFont.Bold))
            empty_label.setPos(start_x + 100, start_y - 50)

    def _draw_queue_pointer(self, x, y, label):
        """绘制队列指针"""
        # 绘制指针线
        line = self.scene.addLine(x, y, x + 20, y)
        line.setPen(QPen(Qt.blue, 3))

        # 绘制箭头
        arrow = self.scene.addPolygon(
            QPolygonF([QPointF(x + 20, y),
                       QPointF(x + 10, y - 5),
                       QPointF(x + 10, y + 5)]))
        arrow.setBrush(QBrush(Qt.blue))

        # 添加标签
        text = self.scene.addText(label)
        text.setDefaultTextColor(Qt.blue)
        text.setFont(QFont("Arial", 10))
        text.setPos(x, y - 25)

    def draw_binary_tree(self, tree):
        """绘制二叉树"""
        self.clear_scene()

        tree_structure = tree.get_tree_structure()
        if tree_structure is None:
            empty_label = self.scene.addText("二叉树为空")
            empty_label.setDefaultTextColor(Qt.red)
            empty_label.setFont(QFont("Arial", 14, QFont.Bold))
            empty_label.setPos(350, 200)
            return

        # 计算树的高度和节点位置
        height = self._calculate_tree_height(tree_structure)
        positions = {}
        self._calculate_node_positions(tree_structure, 400, 50, 300, height, positions)

        # 绘制连线
        self._draw_tree_connections(tree_structure, positions)

        # 绘制节点
        self._draw_tree_nodes(tree_structure, positions)

    def _calculate_tree_height(self, node):
        """计算树的高度"""
        if node is None:
            return 0
        left_height = self._calculate_tree_height(node['left'])
        right_height = self._calculate_tree_height(node['right'])
        return max(left_height, right_height) + 1

    def _calculate_node_positions(self, node, x, y, horizontal_spacing, level, positions):
        """计算每个节点的位置"""
        if node is None:
            return

        positions[node['data']] = (x, y)

        # 计算子节点的垂直间距
        vertical_spacing = 80

        if node['left'] is not None:
            left_x = x - horizontal_spacing / (2 ** (level - 1))
            left_y = y + vertical_spacing
            self._calculate_node_positions(node['left'], left_x, left_y, horizontal_spacing, level - 1, positions)

        if node['right'] is not None:
            right_x = x + horizontal_spacing / (2 ** (level - 1))
            right_y = y + vertical_spacing
            self._calculate_node_positions(node['right'], right_x, right_y, horizontal_spacing, level - 1, positions)

    def _draw_tree_connections(self, node, positions):
        """绘制树的连线"""
        if node is None:
            return

        current_pos = positions.get(node['data'])

        if current_pos and node['left'] is not None:
            left_pos = positions.get(node['left']['data'])
            if left_pos:
                line = self.scene.addLine(current_pos[0], current_pos[1], left_pos[0], left_pos[1])
                line.setPen(QPen(Qt.black, 2))

        if current_pos and node['right'] is not None:
            right_pos = positions.get(node['right']['data'])
            if right_pos:
                line = self.scene.addLine(current_pos[0], current_pos[1], right_pos[0], right_pos[1])
                line.setPen(QPen(Qt.black, 2))

        # 递归绘制子节点的连线
        if node['left'] is not None:
            self._draw_tree_connections(node['left'], positions)

        if node['right'] is not None:
            self._draw_tree_connections(node['right'], positions)

    def _draw_tree_nodes(self, node, positions):
        """绘制树的节点"""
        if node is None:
            return

        pos = positions.get(node['data'])
        if pos:
            x, y = pos
            node_width = 40
            node_height = 40

            # 绘制节点圆形
            ellipse = self.scene.addEllipse(x - node_width / 2, y - node_height / 2, node_width, node_height)
            ellipse.setBrush(QBrush(QColor(255, 182, 193)))  # 浅粉色
            ellipse.setPen(QPen(Qt.black, 2))

            # 绘制节点数据
            text = self.scene.addText(str(node['data']))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 10, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

        # 递归绘制子节点
        if node['left'] is not None:
            self._draw_tree_nodes(node['left'], positions)

        if node['right'] is not None:
            self._draw_tree_nodes(node['right'], positions)