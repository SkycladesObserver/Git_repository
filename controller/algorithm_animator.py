from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor


class AlgorithmAnimator(QObject):
    """算法动画控制器"""

    # 信号：步骤更新、状态变化、完成
    step_started = pyqtSignal(int, str)  # 步骤索引, 描述
    step_finished = pyqtSignal(int, str)  # 步骤索引, 描述
    algorithm_finished = pyqtSignal(str)  # 算法名称
    highlight_nodes = pyqtSignal(list, QColor, str)  # 节点ID列表, 颜色, 描述

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_algorithm = None
        self.steps = []
        self.current_step_index = 0
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_next_step)
        self.animation_speed = 1000

        # 存储高亮状态
        self.highlighted_nodes = {}

    def set_speed(self, speed_ms):
        """设置动画速度"""
        self.animation_speed = speed_ms
        if self.timer.isActive():
            self.timer.setInterval(speed_ms)

    def start_algorithm(self, algorithm_name, data=None):
        """开始算法演示"""
        if self.is_running:
            self.stop_algorithm()

        self.current_algorithm = algorithm_name
        self.steps = self._prepare_algorithm_steps(algorithm_name, data)
        self.current_step_index = 0
        self.is_running = True

        if self.steps:
            self.timer.start(self.animation_speed)
            self._execute_current_step()
        else:
            self.is_running = False

    def stop_algorithm(self):
        """停止算法演示"""
        self.is_running = False
        self.timer.stop()
        self._clear_highlights()
        self.algorithm_finished.emit(self.current_algorithm)

    def pause_algorithm(self):
        """暂停算法演示"""
        self.timer.stop()

    def resume_algorithm(self):
        """继续算法演示"""
        if self.is_running and not self.timer.isActive():
            self.timer.start(self.animation_speed)

    def execute_next_step(self):
        """执行下一步"""
        self.current_step_index += 1
        if self.current_step_index < len(self.steps):
            self._execute_current_step()
        else:
            self.stop_algorithm()

    def _execute_current_step(self):
        """执行当前步骤"""
        if self.current_step_index >= len(self.steps):
            return

        step = self.steps[self.current_step_index]
        step_type = step.get('type')
        description = step.get('description', '')

        print(f"执行步骤 {self.current_step_index}: {step_type} - {description}")  # 调试输出

        self.step_started.emit(self.current_step_index, description)

        # 清除之前的高亮
        self._clear_highlights()

        if step_type == 'highlight':
            # 高亮节点
            node_ids = step.get('node_ids', [])
            color = step.get('color', QColor(255, 255, 0))
            print(f"高亮节点: {node_ids}")  # 调试输出
            self._highlight_nodes(node_ids, color, description)

        elif step_type == 'operation':
            # 执行操作
            operation = step.get('operation')
            operation_data = step.get('data', {})
            print(f"执行操作: {operation}")  # 调试输出
            self._execute_operation(operation, operation_data)

        elif step_type == 'message':
            # 只显示消息
            print(f"显示消息: {description}")  # 调试输出
            self.main_window.status_bar.showMessage(description)

        # 强制更新显示
        self.main_window.update_display(description)

        self.step_finished.emit(self.current_step_index, description)
    def _highlight_nodes(self, node_ids, color, description):
        """高亮节点"""
        self.highlighted_nodes = {node_id: color for node_id in node_ids}
        self.highlight_nodes.emit(node_ids, color, description)

    def _clear_highlights(self):
        """清除高亮"""
        if self.highlighted_nodes:
            self.highlight_nodes.emit([], QColor(255, 255, 255), "")
            self.highlighted_nodes = {}

    def _execute_operation(self, operation, data):
        """执行操作"""
        try:
            if operation == 'bst_search_step':
                # 二叉搜索树查找步骤
                value = data['value']
                current_node_id = data.get('current_node')
                found = data.get('found', False)

                # 这里可以添加查找逻辑，更新当前节点状态
                self.main_window.status_bar.showMessage(f"查找 {value}, 当前节点: {current_node_id}")

            elif operation == 'huffman_merge':
                # 哈夫曼合并步骤
                node1 = data['node1']
                node2 = data['node2']
                new_node = data['new_node']

                # 执行合并操作
                self.main_window.huffman_tree._merge_nodes(node1, node2, new_node)

            elif operation == 'avl_rotate':
                # AVL旋转步骤
                rotation_type = data['type']  # 'left', 'right', 'left_right', 'right_left'
                nodes_involved = data['nodes']

                # 执行旋转操作
                self._perform_avl_rotation(rotation_type, nodes_involved)

        except Exception as e:
            print(f"操作执行错误: {e}")

    def _prepare_algorithm_steps(self, algorithm_name, data):
        """准备算法步骤"""
        steps = []

        if algorithm_name == "bst_search":
            # 二叉搜索树查找步骤
            target_value = data.get('value', 50)
            steps = self._prepare_bst_search_steps(target_value)

        elif algorithm_name == "huffman_build":
            # 哈夫曼树构建步骤
            text = data.get('text', 'example')
            steps = self._prepare_huffman_build_steps(text)

        elif algorithm_name == "avl_insert":
            # AVL树插入步骤
            values = data.get('values', [10, 20, 30])
            steps = self._prepare_avl_insert_steps(values)

        elif algorithm_name == "avl_delete":
            # AVL树删除步骤
            value = data.get('value', 20)
            steps = self._prepare_avl_delete_steps(value)

        return steps

    def _prepare_bst_search_steps(self, target_value):
        """准备二叉搜索树查找步骤"""
        steps = []
        bst = self.main_window.bst

        # 模拟查找过程
        def search_steps(node, value, path=[]):
            if node is None:
                return

            node_id = node.data['id']
            path.append(node_id)

            # 高亮当前访问的节点
            steps.append({
                'type': 'highlight',
                'node_ids': [node_id],
                'color': QColor(255, 200, 100),  # 橙色
                'description': f'访问节点 {node.data["value"]}'
            })

            if value == node.data['value']:
                # 找到目标
                steps.append({
                    'type': 'highlight',
                    'node_ids': [node_id],
                    'color': QColor(100, 255, 100),  # 绿色
                    'description': f'找到目标值 {value}'
                })
                return True
            elif value < node.data['value']:
                steps.append({
                    'type': 'message',
                    'description': f'{value} < {node.data["value"]}, 转向左子树'
                })
                return search_steps(node.left, value, path)
            else:
                steps.append({
                    'type': 'message',
                    'description': f'{value} > {node.data["value"]}, 转向右子树'
                })
                return search_steps(node.right, value, path)

        # 开始查找
        steps.append({
            'type': 'message',
            'description': f'开始查找值 {target_value}'
        })

        if bst.root:
            found = search_steps(bst.root, target_value)
            if not found:
                steps.append({
                    'type': 'message',
                    'description': f'未找到值 {target_value}'
                })
        else:
            steps.append({
                'type': 'message',
                'description': '二叉搜索树为空'
            })

        return steps

    def _prepare_huffman_build_steps(self, text):
        """准备哈夫曼树构建步骤"""
        steps = []

        # 计算字符频率
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1

        steps.append({
            'type': 'message',
            'description': f'文本 "{text}" 的字符频率: {frequency}'
        })

        # 创建叶子节点
        nodes = []
        for char, freq in frequency.items():
            node_id = f"huffman_leaf_{char}"
            nodes.append({'id': node_id, 'char': char, 'freq': freq})

            steps.append({
                'type': 'highlight',
                'node_ids': [node_id],
                'color': QColor(200, 230, 255),
                'description': f'创建叶子节点: 字符 "{char}", 频率 {freq}'
            })

        # 模拟构建过程（简化版）
        steps.append({
            'type': 'message',
            'description': '开始构建哈夫曼树，重复选择两个最小频率的节点合并'
        })

        # 这里可以添加更详细的构建步骤...

        steps.append({
            'type': 'message',
            'description': '哈夫曼树构建完成'
        })

        return steps

    def _prepare_avl_insert_steps(self, values):
        """准备AVL树插入步骤"""
        steps = []

        steps.append({
            'type': 'message',
            'description': f'开始插入值: {values}'
        })

        for i, value in enumerate(values):
            steps.append({
                'type': 'message',
                'description': f'步骤 {i + 1}: 插入值 {value}'
            })

            # 模拟插入过程，检测是否需要旋转
            # 这里可以添加详细的插入和旋转步骤...

            if value == 20:  # 示例：当插入20时可能需要旋转
                steps.extend(self._prepare_avl_rotation_steps('left_rotate'))

        steps.append({
            'type': 'message',
            'description': 'AVL树插入完成'
        })

        return steps

    def _prepare_avl_rotation_steps(self, rotation_type):
        """准备AVL旋转步骤"""
        steps = []

        rotation_names = {
            'left_rotate': '左旋转',
            'right_rotate': '右旋转',
            'left_right_rotate': '左右旋转',
            'right_left_rotate': '右左旋转'
        }

        steps.append({
            'type': 'message',
            'description': f'检测到不平衡，执行{rotation_names.get(rotation_type, rotation_type)}'
        })

        # 这里可以添加旋转的详细步骤...

        steps.append({
            'type': 'message',
            'description': f'{rotation_names.get(rotation_type, rotation_type)}完成'
        })

        return steps

    def _prepare_avl_delete_steps(self, value):
        """准备AVL树删除步骤"""
        steps = []

        steps.append({
            'type': 'message',
            'description': f'开始删除值 {value}'
        })

        # 这里可以添加删除的详细步骤...

        steps.append({
            'type': 'message',
            'description': f'值 {value} 删除完成'
        })

        return steps

    def _perform_avl_rotation(self, rotation_type, nodes):
        """执行AVL旋转"""
        # 这里实现具体的旋转逻辑
        pass

    # 在 algorithm_animator.py 中添加测试算法
    def _prepare_test_algorithm(self):
        """准备测试算法步骤"""
        steps = [
            {
                'type': 'message',
                'description': '开始测试算法演示'
            },
            {
                'type': 'highlight',
                'node_ids': ['test_node_1'],
                'color': QColor(255, 0, 0),  # 红色
                'description': '高亮第一个节点'
            },
            {
                'type': 'message',
                'description': '等待1秒...'
            },
            {
                'type': 'highlight',
                'node_ids': ['test_node_2'],
                'color': QColor(0, 255, 0),  # 绿色
                'description': '高亮第二个节点'
            },
            {
                'type': 'message',
                'description': '测试完成'
            }
        ]
        return steps