
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

        # 添加高亮支持
        self.highlighted_nodes = {}  # {node_id: color}

        # 设置背景
        self.setStyleSheet("background-color: #f5f5f5; border: 1px solid #cccccc;")

    def highlight_nodes(self, node_ids, color, description=""):
        """高亮指定的节点"""
        print(f"GraphicsView: 高亮节点 {node_ids} 颜色 {color}")  # 调试输出
        self.highlighted_nodes = {node_id: color for node_id in node_ids}
        
        # 显示操作描述文本
        if description:
            self._show_operation_text(description)

        # 强制重绘整个场景
        self._redraw_current_structure()
    
    def _show_operation_text(self, text, duration=2000):
        """显示操作说明文本"""
        # 清除之前的文本
        for item in self.scene.items():
            if hasattr(item, 'is_operation_text') and item.is_operation_text:
                self.scene.removeItem(item)
        
        # 添加新文本
        text_item = self.scene.addText(text)
        text_item.setDefaultTextColor(QColor(0, 100, 200))
        text_item.setFont(QFont("Arial", 12, QFont.Bold))
        text_item.setPos(50, 20)
        text_item.is_operation_text = True
        
        # 设置定时器自动清除
        QTimer.singleShot(duration, lambda: self._clear_operation_text())
    
    def _clear_operation_text(self):
        """清除操作文本"""
        for item in self.scene.items():
            if hasattr(item, 'is_operation_text') and item.is_operation_text:
                self.scene.removeItem(item)

    def clear_highlights(self):
        """清除所有高亮"""
        self.highlighted_nodes = {}
        self._redraw_current_structure()

    def _redraw_current_structure(self):
        """根据当前数据结构重新绘制"""
        # 清空场景
        self.scene.clear()

        # 根据主窗口的当前数据结构重新绘制
        main_window = self.parent()
        if hasattr(main_window, 'current_ds'):
            current_ds = main_window.current_ds

            if current_ds == "链表":
                if hasattr(main_window, 'linked_list') and main_window.linked_list.head is not None:
                    self.draw_linked_list(main_window.linked_list)
            elif current_ds == "栈":
                if hasattr(main_window, 'stack'):
                    self.draw_stack(main_window.stack)
            elif current_ds == "队列":
                if hasattr(main_window, 'queue'):
                    self.draw_queue(main_window.queue)
            elif current_ds == "二叉树":
                if hasattr(main_window, 'binary_tree'):
                    self.draw_binary_tree(main_window.binary_tree)
            elif current_ds == "二叉搜索树":
                if hasattr(main_window, 'bst'):
                    self.draw_binary_search_tree(main_window.bst)
            elif current_ds == "哈夫曼树":
                if hasattr(main_window, 'huffman_tree'):
                    self.draw_huffman_tree(main_window.huffman_tree)
            elif current_ds == "AVL树":
                if hasattr(main_window, 'avl_tree'):
                    self.draw_avl_tree(main_window.avl_tree)

    # 修改绘制方法，在绘制节点时检查高亮状态
    def _draw_tree_nodes(self, node, positions):
        """绘制树的节点，支持高亮"""
        if node is None:
            return

        pos = positions.get(node['id'])
        if pos:
            x, y = pos
            node_width = 40
            node_height = 40

            # 检查是否需要高亮
            highlight_color = self.highlighted_nodes.get(node['id'])
            if highlight_color:
                # 使用高亮颜色
                node_color = highlight_color
                border_color = Qt.red
                border_width = 3
            else:
                # 默认颜色
                node_color = QColor(255, 182, 193)  # 浅粉色
                border_color = Qt.black
                border_width = 2

            # 绘制节点圆形
            ellipse = self.scene.addEllipse(x - node_width / 2, y - node_height / 2, node_width, node_height)
            ellipse.setBrush(QBrush(node_color))
            ellipse.setPen(QPen(border_color, border_width))

            # 绘制节点数据
            text = self.scene.addText(str(node['data']))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 10, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

        # 递归绘制子节点
        if node.get('left') is not None:
            self._draw_tree_nodes(node['left'], positions)
        if node.get('right') is not None:
            self._draw_tree_nodes(node['right'], positions)

    def draw_linked_list(self, linked_list):
        """绘制链表"""
        self.clear_scene()
        self.node_items = []

        # 收集节点对象和位置信息
        node_objects = []
        current = linked_list.head
        while current:
            node_objects.append(current)
            current = current.next

        # 计算布局
        node_width = 80
        node_height = 50
        horizontal_spacing = 100
        start_x = 50
        start_y = 200

        # 绘制节点和连线
        for i, node_obj in enumerate(node_objects):
            x = start_x + i * (node_width + horizontal_spacing)
            y = start_y
            data = node_obj.data
            node_id = id(node_obj)  # 使用节点对象的内存地址作为ID

            # 检查是否需要高亮
            highlight_color = self.highlighted_nodes.get(node_id)
            if highlight_color:
                node_color = highlight_color
                border_color = Qt.red
                border_width = 3
            else:
                node_color = QColor(173, 216, 230)  # 浅蓝色
                border_color = Qt.black
                border_width = 2

            # 创建图形节点
            node_item = NodeGraphicsItem(data, x, y, node_width, node_height)
            self.node_items.append(node_item)

            # 绘制节点矩形
            rect = self.scene.addRect(x, y, node_width, node_height)
            rect.setBrush(QBrush(node_color))
            rect.setPen(QPen(border_color, border_width))

            # 绘制节点数据
            text = self.scene.addText(str(data))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 12, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x + node_width / 2 - text_rect.width() / 2,
                        y + node_height / 2 - text_rect.height() / 2)

            # 如果不是最后一个节点，绘制箭头
            if i < len(node_objects) - 1:
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

        # 检查是否需要高亮栈顶
        highlight_top = 'stack_top' in self.highlighted_nodes

        # 绘制栈元素（从底部到顶部）
        for i in range(stack.capacity):
            x = start_x
            y = start_y + (stack.capacity - 1 - i) * (element_height + spacing)

            # 绘制栈元素背景
            rect = self.scene.addRect(x, y, element_width, element_height)

            if i <= stack.top:
                # 有数据的元素
                # 检查是否是栈顶且需要高亮
                if i == stack.top and highlight_top:
                    highlight_color = self.highlighted_nodes.get('stack_top')
                    rect.setBrush(QBrush(highlight_color))
                    rect.setPen(QPen(Qt.red, 3))
                else:
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

        # 检查是否需要高亮队头或队尾
        highlight_front = 'queue_front' in self.highlighted_nodes
        highlight_rear = 'queue_rear' in self.highlighted_nodes

        # 绘制队列框架
        frame_width = len(queue_data) * (element_width + spacing) if queue_data else element_width
        frame = self.scene.addRect(start_x - 10, start_y - 10,
                                   frame_width + 20, element_height + 20)
        frame.setPen(QPen(Qt.black, 2))

        # 绘制队列元素
        for i, data in enumerate(queue_data):
            x = start_x + i * (element_width + spacing)
            y = start_y

            # 检查是否需要高亮
            is_front = (i == 0) and highlight_front
            is_rear = (i == len(queue_data) - 1) and highlight_rear
            
            if is_front:
                highlight_color = self.highlighted_nodes.get('queue_front')
                rect_color = highlight_color
                border_color = Qt.red
                border_width = 3
            elif is_rear:
                highlight_color = self.highlighted_nodes.get('queue_rear')
                rect_color = highlight_color
                border_color = Qt.red
                border_width = 3
            else:
                rect_color = QColor(255, 218, 185)  # 桃色
                border_color = Qt.black
                border_width = 2

            # 绘制队列元素背景
            rect = self.scene.addRect(x, y, element_width, element_height)
            rect.setBrush(QBrush(rect_color))
            rect.setPen(QPen(border_color, border_width))

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
        """绘制二叉树 - 使用改进的布局算法"""
        self.clear_scene()

        tree_structure = tree.get_tree_structure()
        if tree_structure is None:
            empty_label = self.scene.addText("二叉树为空")
            empty_label.setDefaultTextColor(Qt.red)
            empty_label.setFont(QFont("Arial", 14, QFont.Bold))
            empty_label.setPos(350, 200)
            return

        # 使用改进的布局算法计算节点位置
        positions = self.calculate_tree_layout(tree_structure)

        # 绘制连线
        self._draw_tree_connections(tree_structure, positions)

        # 绘制节点
        self._draw_tree_nodes(tree_structure, positions)

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

    def draw_binary_search_tree(self, bst):
        """绘制二叉搜索树 - 使用改进的布局算法"""
        self.clear_scene()

        tree_structure = bst.get_tree_structure()
        if tree_structure is None:
            empty_label = self.scene.addText("二叉搜索树为空")
            empty_label.setDefaultTextColor(Qt.red)
            empty_label.setFont(QFont("Arial", 14, QFont.Bold))
            empty_label.setPos(350, 200)
            return

        # 使用改进的布局算法计算节点位置
        positions = self.calculate_tree_layout(tree_structure)

        # 绘制连线
        self._draw_tree_connections(tree_structure, positions)

        # 绘制节点
        self._draw_bst_nodes(tree_structure, positions)

    def _calculate_tree_layout(self, node, x, y, base_spacing, total_height, positions):
        """改进的树形布局算法 - 使用唯一标识符"""
        if node is None:
            return

        # 使用节点的唯一标识符作为键
        positions[node['id']] = (x, y)

        # 计算当前节点的深度
        current_depth = self._calculate_node_depth(node, total_height)

        # 动态调整水平间距：上层节点间距大，下层节点间距小
        horizontal_spacing = base_spacing * (0.7 ** current_depth)
        vertical_spacing = 80

        if node['left'] is not None:
            left_x = x - horizontal_spacing
            left_y = y + vertical_spacing
            self._calculate_tree_layout(node['left'], left_x, left_y, base_spacing, total_height, positions)

        if node['right'] is not None:
            right_x = x + horizontal_spacing
            right_y = y + vertical_spacing
            self._calculate_tree_layout(node['right'], right_x, right_y, base_spacing, total_height, positions)

    def calculate_tree_layout(self, tree_structure):
        """使用改进的树布局算法计算节点位置"""
        if tree_structure is None:
            return {}

        # 第一步：计算每个节点的尺寸和位置
        positions = {}
        self._layout_tree(tree_structure, positions)

        # 第二步：居中整个树
        self._center_tree(positions)

        return positions

    def _layout_tree(self, node, positions, x=0, y=0, depth=0):
        """递归计算树布局"""
        if node is None:
            return 0

        # 计算左子树和右子树的宽度
        left_width = self._layout_tree(node.get('left'), positions, x, y + 1, depth + 1)
        right_width = self._layout_tree(node.get('right'), positions, x + left_width + 1, y + 1, depth + 1)

        # 当前节点的x位置是左子树宽度 + 0.5（居中）
        node_x = x + left_width

        # 存储节点位置
        positions[node['id']] = (node_x * 80 + 100, y * 100 + 100)  # 调整间距

        # 返回当前子树的宽度
        return left_width + right_width + 1

    def _center_tree(self, positions):
        """将树居中显示"""
        if not positions:
            return

        # 找到x坐标的最小值和最大值
        x_values = [pos[0] for pos in positions.values()]
        min_x, max_x = min(x_values), max(x_values)

        # 计算居中偏移量
        center_x = 400  # 画布中心
        tree_center = (min_x + max_x) / 2
        offset_x = center_x - tree_center

        # 应用偏移量
        for node_id in positions:
            x, y = positions[node_id]
            positions[node_id] = (x + offset_x, y)

    def _calculate_node_depth(self, node, total_height):
        """计算节点在树中的深度"""
        if node is None:
            return 0

        # 通过递归计算节点到根节点的距离
        def get_depth(current_node, current_depth):
            if current_node is None:
                return current_depth

            left_depth = get_depth(current_node.get('left'), current_depth + 1)
            right_depth = get_depth(current_node.get('right'), current_depth + 1)

            return max(left_depth, right_depth)

        return get_depth(node, 0)

    def _calculate_tree_height(self, node):
        """计算树的高度"""
        if node is None:
            return 0

        left_height = self._calculate_tree_height(node['left'])
        right_height = self._calculate_tree_height(node['right'])

        return max(left_height, right_height) + 1

    def _draw_tree_connections(self, node, positions):
        """绘制树的连线"""
        if node is None:
            return

        current_pos = positions.get(node['id'])

        if current_pos and node.get('left') is not None:
            left_pos = positions.get(node['left']['id'])
            if left_pos:
                # 绘制从父节点到左子节点的连线
                line = self.scene.addLine(current_pos[0], current_pos[1], left_pos[0], left_pos[1])
                line.setPen(QPen(Qt.black, 2))

        if current_pos and node.get('right') is not None:
            right_pos = positions.get(node['right']['id'])
            if right_pos:
                # 绘制从父节点到右子节点的连线
                line = self.scene.addLine(current_pos[0], current_pos[1], right_pos[0], right_pos[1])
                line.setPen(QPen(Qt.black, 2))

        # 递归绘制子节点的连线
        if node.get('left') is not None:
            self._draw_tree_connections(node['left'], positions)

        if node.get('right') is not None:
            self._draw_tree_connections(node['right'], positions)

    def _draw_tree_nodes(self, node, positions):
        """绘制树的节点"""
        if node is None:
            return

        pos = positions.get(node['id'])
        if pos:
            x, y = pos
            node_width = 40
            node_height = 40

            # 检查是否需要高亮
            highlight_color = self.highlighted_nodes.get(node['id'])
            if highlight_color:
                node_color = highlight_color
                border_color = Qt.red
                border_width = 3
            else:
                node_color = QColor(255, 182, 193)  # 浅粉色
                border_color = Qt.black
                border_width = 2

            # 绘制节点圆形
            ellipse = self.scene.addEllipse(x - node_width / 2, y - node_height / 2, node_width, node_height)
            ellipse.setBrush(QBrush(node_color))
            ellipse.setPen(QPen(border_color, border_width))

            # 绘制节点数据
            text = self.scene.addText(str(node['data']))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 10, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

        # 递归绘制子节点
        if node.get('left') is not None:
            self._draw_tree_nodes(node['left'], positions)

        if node.get('right') is not None:
            self._draw_tree_nodes(node['right'], positions)

    def _draw_bst_nodes(self, node, positions):
        """绘制BST的节点（使用不同颜色）"""
        if node is None:
            return

        pos = positions.get(node['id'])
        if pos:
            x, y = pos
            node_width = 40
            node_height = 40

            # 检查是否需要高亮
            highlight_color = self.highlighted_nodes.get(node['id'])
            if highlight_color:
                node_color = highlight_color
                border_color = Qt.red
                border_width = 3
            else:
                node_color = QColor(152, 251, 152)  # 浅绿色
                border_color = Qt.black
                border_width = 2

            # 绘制节点圆形 - 使用不同颜色区分BST
            ellipse = self.scene.addEllipse(x - node_width / 2, y - node_height / 2, node_width, node_height)
            ellipse.setBrush(QBrush(node_color))
            ellipse.setPen(QPen(border_color, border_width))

            # 绘制节点数据
            text = self.scene.addText(str(node['data']))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 10, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

        # 递归绘制子节点
        if node.get('left') is not None:
            self._draw_bst_nodes(node['left'], positions)

        if node.get('right') is not None:
            self._draw_bst_nodes(node['right'], positions)

    def draw_huffman_tree(self, huffman_tree):
        """绘制哈夫曼树"""
        self.clear_scene()

        tree_structure = huffman_tree.get_tree_structure()
        if tree_structure is None:
            empty_label = self.scene.addText("哈夫曼树为空")
            empty_label.setDefaultTextColor(Qt.red)
            empty_label.setFont(QFont("Arial", 14, QFont.Bold))
            empty_label.setPos(350, 200)
            return

        # 使用改进的布局算法计算节点位置
        positions = self.calculate_tree_layout(tree_structure)

        # 绘制连线
        self._draw_huffman_connections(tree_structure, positions)

        # 绘制节点
        self._draw_huffman_nodes(tree_structure, positions)

        # 显示编码表
        self._display_huffman_codes(huffman_tree.get_codes())

    def _draw_huffman_connections(self, node, positions):
        """绘制哈夫曼树的连线，并标注0/1"""
        if node is None:
            return

        current_pos = positions.get(node['id'])

        if current_pos and node.get('left') is not None:
            left_pos = positions.get(node['left']['id'])
            if left_pos:
                # 绘制从父节点到左子节点的连线
                line = self.scene.addLine(current_pos[0], current_pos[1], left_pos[0], left_pos[1])
                line.setPen(QPen(Qt.black, 2))

                # 在连线中间标注"0"
                mid_x = (current_pos[0] + left_pos[0]) / 2
                mid_y = (current_pos[1] + left_pos[1]) / 2
                zero_text = self.scene.addText("0")
                zero_text.setDefaultTextColor(Qt.blue)
                zero_text.setFont(QFont("Arial", 10, QFont.Bold))
                zero_text.setPos(mid_x, mid_y)

        if current_pos and node.get('right') is not None:
            right_pos = positions.get(node['right']['id'])
            if right_pos:
                # 绘制从父节点到右子节点的连线
                line = self.scene.addLine(current_pos[0], current_pos[1], right_pos[0], right_pos[1])
                line.setPen(QPen(Qt.black, 2))

                # 在连线中间标注"1"
                mid_x = (current_pos[0] + right_pos[0]) / 2
                mid_y = (current_pos[1] + right_pos[1]) / 2
                one_text = self.scene.addText("1")
                one_text.setDefaultTextColor(Qt.blue)
                one_text.setFont(QFont("Arial", 10, QFont.Bold))
                one_text.setPos(mid_x, mid_y)

        # 递归绘制子节点的连线
        if node.get('left') is not None:
            self._draw_huffman_connections(node['left'], positions)

        if node.get('right') is not None:
            self._draw_huffman_connections(node['right'], positions)

    def _draw_huffman_nodes(self, node, positions):
        """绘制哈夫曼树的节点"""
        if node is None:
            return

        pos = positions.get(node['id'])
        if pos:
            x, y = pos
            node_width = 60
            node_height = 40

            # 根据节点类型选择颜色
            if node.get('is_leaf', False):
                color = QColor(255, 200, 150)  # 叶子节点 - 橙色
            else:
                color = QColor(200, 200, 255)  # 内部节点 - 淡蓝色

            # 绘制节点矩形
            rect = self.scene.addRect(x - node_width / 2, y - node_height / 2, node_width, node_height)
            rect.setBrush(QBrush(color))
            rect.setPen(QPen(Qt.black, 2))

            # 绘制节点数据
            text = self.scene.addText(str(node['data']))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 9, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

        # 递归绘制子节点
        if node.get('left') is not None:
            self._draw_huffman_nodes(node['left'], positions)

        if node.get('right') is not None:
            self._draw_huffman_nodes(node['right'], positions)

    def _display_huffman_codes(self, codes):
        """显示哈夫曼编码表"""
        if not codes:
            return

        # 在右侧显示编码表
        x_pos = 650
        y_pos = 50

        title = self.scene.addText("哈夫曼编码表:")
        title.setDefaultTextColor(Qt.darkBlue)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setPos(x_pos, y_pos)

        y_pos += 30

        for char, code in codes.items():
            # 处理特殊字符（如空格、换行符等）
            display_char = char
            if char == ' ':
                display_char = "' '"
            elif char == '\n':
                display_char = "\\n"
            elif char == '\t':
                display_char = "\\t"

            code_text = self.scene.addText(f"{display_char}: {code}")
            code_text.setDefaultTextColor(Qt.darkGreen)
            code_text.setFont(QFont("Arial", 10))
            code_text.setPos(x_pos, y_pos)
            y_pos += 20

    def draw_avl_tree(self, avl_tree):
        """绘制AVL树"""
        self.clear_scene()

        tree_structure = avl_tree.get_tree_structure()
        if tree_structure is None:
            empty_label = self.scene.addText("AVL树为空")
            empty_label.setDefaultTextColor(Qt.red)
            empty_label.setFont(QFont("Arial", 14, QFont.Bold))
            empty_label.setPos(350, 200)
            return

        # 使用改进的布局算法计算节点位置
        positions = self.calculate_tree_layout(tree_structure)

        # 绘制连线
        self._draw_tree_connections(tree_structure, positions)

        # 绘制节点
        self._draw_avl_nodes(tree_structure, positions)

        # 显示AVL树说明
        self._display_avl_info()

    def _draw_avl_nodes(self, node, positions):
        """绘制AVL树的节点，显示平衡因子"""
        if node is None:
            return

        pos = positions.get(node['id'])
        if pos:
            x, y = pos
            node_width = 50
            node_height = 50

            # 检查是否需要高亮
            highlight_color = self.highlighted_nodes.get(node['id'])
            if highlight_color:
                node_color = highlight_color
                border_color = Qt.red
                border_width = 3
            else:
                # 根据平衡因子选择颜色
                balance = node.get('balance', 0)
                if balance == 0:
                    node_color = QColor(144, 238, 144)  # 平衡 - 浅绿色
                elif abs(balance) == 1:
                    node_color = QColor(255, 255, 150)  # 基本平衡 - 浅黄色
                else:
                    node_color = QColor(255, 150, 150)  # 不平衡 - 浅红色
                border_color = Qt.black
                border_width = 2

            # 绘制节点圆形
            ellipse = self.scene.addEllipse(x - node_width / 2, y - node_height / 2, node_width, node_height)
            ellipse.setBrush(QBrush(node_color))
            ellipse.setPen(QPen(border_color, border_width))

            # 绘制节点数据（值和平衡因子）
            text = self.scene.addText(str(node['data']))
            text.setDefaultTextColor(Qt.black)
            text.setFont(QFont("Arial", 9, QFont.Bold))
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)

        # 递归绘制子节点
        if node.get('left') is not None:
            self._draw_avl_nodes(node['left'], positions)

        if node.get('right') is not None:
            self._draw_avl_nodes(node['right'], positions)

    def _display_avl_info(self):
        """显示AVL树说明"""
        x_pos = 650
        y_pos = 50

        title = self.scene.addText("AVL树说明:")
        title.setDefaultTextColor(Qt.darkBlue)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setPos(x_pos, y_pos)

        y_pos += 30

        info_lines = [
            "平衡因子 = 左子树高度 - 右子树高度",
            "平衡: 绿色 (平衡因子 = 0)",
            "基本平衡: 黄色 (平衡因子 = ±1)",
            "不平衡: 红色 (平衡因子 = ±2)",
            "",
            "旋转操作:",
            "- 左左情况: 右旋转",
            "- 右右情况: 左旋转",
            "- 左右情况: 先左旋后右旋",
            "- 右左情况: 先右旋后左旋"
        ]

        for line in info_lines:
            info_text = self.scene.addText(line)
            info_text.setDefaultTextColor(Qt.darkGreen)
            info_text.setFont(QFont("Arial", 9))
            info_text.setPos(x_pos, y_pos)
            y_pos += 20