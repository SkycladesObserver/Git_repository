from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor


class UnifiedAnimationController(QObject):
    """统一的动画控制器，管理所有数据结构的动画演示"""
    
    # 信号定义
    step_changed = pyqtSignal(int, str)  # 步骤索引, 描述
    animation_finished = pyqtSignal()
    status_changed = pyqtSignal(str)  # 状态消息
    highlight_requested = pyqtSignal(list, QColor, str)  # 节点ID列表, 颜色, 描述
    operation_executed = pyqtSignal(str)  # 操作完成信号
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.steps = []  # 动画步骤队列
        self.current_step_index = 0
        self.is_playing = False
        self.is_paused = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._execute_next_step)
        self.animation_speed = 1000  # 默认速度：1秒/步
        
        # 存储操作前的状态快照（用于回退）
        self.state_snapshots = []
        
    def set_animation_speed(self, speed_ms):
        """设置动画速度（毫秒）"""
        self.animation_speed = speed_ms
        if self.timer.isActive():
            self.timer.setInterval(speed_ms)
    
    def add_operation(self, operation_type, operation_data, clear_previous=True):
        """
        添加操作到动画队列
        
        Args:
            operation_type: 操作类型（如 'linked_list_insert', 'bst_insert' 等）
            operation_data: 操作数据字典
            clear_previous: 是否清空之前的操作队列（默认True，只执行当前操作）
        """
        # 如果清空之前的操作，先停止当前动画并清空队列
        if clear_previous:
            self.stop()
            self.clear_steps()
        
        # 根据操作类型生成动画步骤
        steps = self._generate_animation_steps(operation_type, operation_data)
        self.steps.extend(steps)
        
        # 重置当前步骤索引
        self.current_step_index = 0
        
        # 通知主窗口更新进度显示
        total_steps = len(self.steps)
        self.step_changed.emit(self.current_step_index, f"已添加 {len(steps)} 个步骤，总计 {total_steps} 步")
        
        if not self.is_playing and not self.is_paused:
            self.status_changed.emit(f"已添加 {len(steps)} 个动画步骤，请使用'下一步'按钮执行")
    
    def _generate_animation_steps(self, operation_type, operation_data):
        """根据操作类型生成动画步骤"""
        steps = []
        
        if operation_type.startswith('linked_list_'):
            steps = self._generate_linked_list_steps(operation_type, operation_data)
        elif operation_type.startswith('stack_'):
            steps = self._generate_stack_steps(operation_type, operation_data)
        elif operation_type.startswith('queue_'):
            steps = self._generate_queue_steps(operation_type, operation_data)
        elif operation_type.startswith('binary_tree_'):
            steps = self._generate_binary_tree_steps(operation_type, operation_data)
        elif operation_type.startswith('bst_'):
            steps = self._generate_bst_steps(operation_type, operation_data)
        elif operation_type.startswith('avl_'):
            steps = self._generate_avl_steps(operation_type, operation_data)
        elif operation_type.startswith('huffman_'):
            steps = self._generate_huffman_steps(operation_type, operation_data)
        
        return steps
    
    def _generate_linked_list_steps(self, operation_type, data):
        """生成链表操作的动画步骤"""
        steps = []
        ll = self.main_window.linked_list
        
        if operation_type == 'linked_list_insert_beginning':
            value = data.get('value')
            # 步骤1：显示准备插入
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(255, 200, 100),
                'description': f'准备在链表开头插入节点: {value}'
            })
            # 步骤2：高亮当前头节点（如果存在）
            if ll.head:
                steps.append({
                    'type': 'highlight',
                    'nodes': [id(ll.head)],
                    'color': QColor(200, 200, 255),
                    'description': f'当前头节点: {ll.head.data}'
                })
            # 步骤3：执行插入
            steps.append({
                'type': 'execute',
                'action': 'insert_beginning',
                'data': {'value': value},
                'description': f'插入节点: {value}'
            })
            # 步骤4：高亮新插入的节点
            steps.append({
                'type': 'highlight',
                'nodes': [],  # 插入后通过重新绘制获取新节点
                'color': QColor(100, 255, 100),
                'description': f'新节点已插入到开头'
            })
            
        elif operation_type == 'linked_list_insert_end':
            value = data.get('value')
            # 步骤1：遍历到末尾
            if ll.head:
                current = ll.head
                path = []
                while current:
                    path.append(id(current))
                    if current.next:
                        current = current.next
                    else:
                        break
                if len(path) > 1:
                    # 高亮路径中的节点（除了最后一个）
                    steps.append({
                        'type': 'highlight',
                        'nodes': path[:-1],
                        'color': QColor(200, 200, 255),
                        'description': f'遍历链表到末尾'
                    })
                # 高亮最后一个节点
                if path:
                    steps.append({
                        'type': 'highlight',
                        'nodes': [path[-1]],
                        'color': QColor(255, 200, 100),
                        'description': f'到达链表末尾'
                    })
            # 步骤2：执行插入
            steps.append({
                'type': 'execute',
                'action': 'insert_end',
                'data': {'value': value},
                'description': f'在末尾插入节点: {value}'
            })
            
        elif operation_type == 'linked_list_insert_position':
            value = data.get('value')
            position = data.get('position')
            # 步骤1：遍历到指定位置
            if ll.head and position > 0:
                current = ll.head
                path = []
                for i in range(position):
                    if current:
                        path.append(id(current))
                        if i < position - 1 and current.next:
                            current = current.next
                if len(path) > 1:
                    steps.append({
                        'type': 'highlight',
                        'nodes': path[:-1],
                        'color': QColor(200, 200, 255),
                        'description': f'遍历到位置 {position}'
                    })
                if path:
                    steps.append({
                        'type': 'highlight',
                        'nodes': [path[-1]],
                        'color': QColor(255, 200, 100),
                        'description': f'到达位置 {position}'
                    })
            # 步骤2：执行插入
            steps.append({
                'type': 'execute',
                'action': 'insert_position',
                'data': {'value': value, 'position': position},
                'description': f'在位置 {position} 插入节点: {value}'
            })
            
        elif operation_type == 'linked_list_delete_position':
            position = data.get('position')
            # 步骤1：遍历到要删除的节点
            if ll.head:
                current = ll.head
                path = []
                for i in range(position + 1):
                    if current:
                        path.append(id(current))
                        if i < position and current.next:
                            current = current.next
                if len(path) > 1:
                    steps.append({
                        'type': 'highlight',
                        'nodes': path[:-1],
                        'color': QColor(200, 200, 255),
                        'description': f'遍历到位置 {position}'
                    })
                if path:
                    steps.append({
                        'type': 'highlight',
                        'nodes': [path[-1]],
                        'color': QColor(255, 150, 150),
                        'description': f'定位到要删除的节点'
                    })
            # 步骤2：执行删除
            steps.append({
                'type': 'execute',
                'action': 'delete_position',
                'data': {'position': position},
                'description': f'删除位置 {position} 的节点'
            })
            
        elif operation_type == 'linked_list_clear':
            # 高亮所有节点
            if ll.head:
                current = ll.head
                all_nodes = []
                while current:
                    all_nodes.append(id(current))
                    current = current.next
                if all_nodes:
                    steps.append({
                        'type': 'highlight',
                        'nodes': all_nodes,
                        'color': QColor(255, 150, 150),
                        'description': '准备清空链表'
                    })
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空链表'
            })
        
        return steps
    
    def _generate_stack_steps(self, operation_type, data):
        """生成栈操作的动画步骤"""
        steps = []
        stack = self.main_window.stack
        
        if operation_type == 'stack_push':
            value = data.get('value')
            # 步骤1：显示准备入栈
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(255, 200, 100),
                'description': f'准备入栈: {value}'
            })
            # 步骤2：高亮当前栈顶（如果存在）
            if not stack.is_empty():
                steps.append({
                    'type': 'highlight',
                    'nodes': ['stack_top'],
                    'color': QColor(200, 200, 255),
                    'description': f'当前栈顶: {stack.peek()}'
                })
            # 步骤3：执行入栈
            steps.append({
                'type': 'execute',
                'action': 'push',
                'data': {'value': value},
                'description': f'入栈: {value}'
            })
            # 步骤4：高亮新栈顶
            steps.append({
                'type': 'highlight',
                'nodes': ['stack_top'],
                'color': QColor(100, 255, 100),
                'description': f'新栈顶: {value}'
            })
            
        elif operation_type == 'stack_pop':
            # 步骤1：高亮栈顶
            if not stack.is_empty():
                steps.append({
                    'type': 'highlight',
                    'nodes': ['stack_top'],
                    'color': QColor(255, 150, 150),
                    'description': f'定位栈顶元素: {stack.peek()}'
                })
            # 步骤2：执行出栈
            steps.append({
                'type': 'execute',
                'action': 'pop',
                'data': {},
                'description': '出栈'
            })
            
        elif operation_type == 'stack_clear':
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空栈'
            })
        
        return steps
    
    def _generate_queue_steps(self, operation_type, data):
        """生成队列操作的动画步骤"""
        steps = []
        queue = self.main_window.queue
        
        if operation_type == 'queue_enqueue':
            value = data.get('value')
            # 步骤1：显示准备入队
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(255, 200, 100),
                'description': f'准备入队: {value}'
            })
            # 步骤2：高亮当前队尾（如果存在）
            if not queue.is_empty():
                steps.append({
                    'type': 'highlight',
                    'nodes': ['queue_rear'],
                    'color': QColor(200, 200, 255),
                    'description': f'当前队尾位置'
                })
            # 步骤3：执行入队
            steps.append({
                'type': 'execute',
                'action': 'enqueue',
                'data': {'value': value},
                'description': f'入队: {value}'
            })
            # 步骤4：高亮新队尾
            steps.append({
                'type': 'highlight',
                'nodes': ['queue_rear'],
                'color': QColor(100, 255, 100),
                'description': f'新元素已入队: {value}'
            })
            
        elif operation_type == 'queue_dequeue':
            # 步骤1：高亮队头
            if not queue.is_empty():
                steps.append({
                    'type': 'highlight',
                    'nodes': ['queue_front'],
                    'color': QColor(255, 150, 150),
                    'description': f'定位队头元素: {queue.peek()}'
                })
            # 步骤2：执行出队
            steps.append({
                'type': 'execute',
                'action': 'dequeue',
                'data': {},
                'description': '出队'
            })
            
        elif operation_type == 'queue_clear':
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空队列'
            })
        
        return steps
    
    def _generate_binary_tree_steps(self, operation_type, data):
        """生成二叉树操作的动画步骤"""
        steps = []
        
        if operation_type == 'binary_tree_insert':
            value = data.get('value')
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(255, 200, 100),
                'description': f'准备层次插入: {value}'
            })
            steps.append({
                'type': 'execute',
                'action': 'insert_level_order',
                'data': {'value': value},
                'description': f'层次插入: {value}'
            })
            
        elif operation_type == 'binary_tree_clear':
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空二叉树'
            })
        
        return steps
    
    def _generate_bst_steps(self, operation_type, data):
        """生成二叉搜索树操作的动画步骤"""
        steps = []
        bst = self.main_window.bst
        
        if operation_type == 'bst_insert':
            value = data.get('value')
            # 生成查找路径的步骤
            path_steps = self._generate_bst_search_path(bst, value, is_insert=True)
            steps.extend(path_steps)
            # 最后执行插入
            steps.append({
                'type': 'execute',
                'action': 'insert',
                'data': {'value': value},
                'description': f'插入节点: {value}'
            })
            
        elif operation_type == 'bst_search':
            value = data.get('value')
            path_steps = self._generate_bst_search_path(bst, value, is_insert=False)
            steps.extend(path_steps)
            
        elif operation_type == 'bst_delete':
            value = data.get('value')
            # 先查找节点
            path_steps = self._generate_bst_search_path(bst, value, is_insert=False)
            steps.extend(path_steps)
            # 执行删除
            steps.append({
                'type': 'execute',
                'action': 'delete',
                'data': {'value': value},
                'description': f'删除节点: {value}'
            })
            
        elif operation_type == 'bst_clear':
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空二叉搜索树'
            })
        
        return steps
    
    def _generate_bst_search_path(self, bst, value, is_insert=False):
        """生成BST查找路径的动画步骤"""
        steps = []
        path = []
        current_node_values = []  # 存储访问的节点值，用于描述
        
        def traverse(node, target_value):
            """遍历查找路径"""
            if node is None:
                return False
            
            node_id = node.data.get('id') if isinstance(node.data, dict) else None
            node_value = node.data.get('value') if isinstance(node.data, dict) else node.data
            
            if node_id:
                path.append(node_id)
                current_node_values.append(node_value)
            
            if target_value == node_value:
                return True
            elif target_value < node_value:
                if node.left:
                    return traverse(node.left, target_value)
                else:
                    return False  # 找到插入位置（左子树为空）
            else:
                if node.right:
                    return traverse(node.right, target_value)
                else:
                    return False  # 找到插入位置（右子树为空）
        
        if bst.root:
            found = traverse(bst.root, value)
            # 为路径中的每个节点生成高亮步骤
            for i, (node_id, node_value) in enumerate(zip(path, current_node_values)):
                if i < len(path) - 1:
                    # 中间节点：显示比较过程
                    steps.append({
                        'type': 'highlight',
                        'nodes': [node_id],
                        'color': QColor(255, 200, 100),
                        'description': f'访问节点 {node_value}，比较 {value} {"<" if value < node_value else ">"} {node_value}'
                    })
                else:
                    # 最后一个节点：显示找到位置或目标
                    if found and not is_insert:
                        steps.append({
                            'type': 'highlight',
                            'nodes': [node_id],
                            'color': QColor(100, 255, 100),
                            'description': f'找到目标值: {value}'
                        })
                    elif not found and not is_insert:
                        steps.append({
                            'type': 'highlight',
                            'nodes': [node_id],
                            'color': QColor(255, 100, 100),
                            'description': f'未找到值: {value}'
                        })
                    else:
                        # 插入操作：显示找到插入位置
                        steps.append({
                            'type': 'highlight',
                            'nodes': [node_id],
                            'color': QColor(200, 200, 255),
                            'description': f'找到插入位置，{value} 将插入到节点 {node_value} 的{"左" if value < node_value else "右"}子树'
                        })
        else:
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(200, 200, 255),
                'description': f'树为空，{value} 将作为根节点插入'
            })
        
        return steps
    
    def _generate_avl_steps(self, operation_type, data):
        """生成AVL树操作的动画步骤"""
        steps = []
        avl = self.main_window.avl_tree
        
        if operation_type == 'avl_insert':
            value = data.get('value')
            # 类似BST的查找路径
            path_steps = self._generate_avl_search_path(avl, value, is_insert=True)
            steps.extend(path_steps)
            steps.append({
                'type': 'execute',
                'action': 'insert',
                'data': {'value': value},
                'description': f'插入节点: {value}（可能需要旋转平衡）'
            })
            
        elif operation_type == 'avl_search':
            value = data.get('value')
            path_steps = self._generate_avl_search_path(avl, value, is_insert=False)
            steps.extend(path_steps)
            
        elif operation_type == 'avl_delete':
            value = data.get('value')
            path_steps = self._generate_avl_search_path(avl, value, is_insert=False)
            steps.extend(path_steps)
            steps.append({
                'type': 'execute',
                'action': 'delete',
                'data': {'value': value},
                'description': f'删除节点: {value}（可能需要旋转平衡）'
            })
            
        elif operation_type == 'avl_clear':
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空AVL树'
            })
        
        return steps
    
    def _generate_avl_search_path(self, avl, value, is_insert=False):
        """生成AVL查找路径的动画步骤"""
        steps = []
        path = []
        current_node_values = []
        
        def traverse(node, target_value):
            """遍历查找路径"""
            if node is None:
                return False
            
            node_id = node.data.get('id') if isinstance(node.data, dict) else None
            node_value = node.data.get('value') if isinstance(node.data, dict) else node.data
            
            if node_id:
                path.append(node_id)
                current_node_values.append(node_value)
            
            if target_value == node_value:
                return True
            elif target_value < node_value:
                if node.left:
                    return traverse(node.left, target_value)
                else:
                    return False
            else:
                if node.right:
                    return traverse(node.right, target_value)
                else:
                    return False
        
        if avl.root:
            found = traverse(avl.root, value)
            for i, (node_id, node_value) in enumerate(zip(path, current_node_values)):
                if i < len(path) - 1:
                    steps.append({
                        'type': 'highlight',
                        'nodes': [node_id],
                        'color': QColor(255, 200, 100),
                        'description': f'访问节点 {node_value}，比较 {value} {"<" if value < node_value else ">"} {node_value}'
                    })
                else:
                    if found and not is_insert:
                        steps.append({
                            'type': 'highlight',
                            'nodes': [node_id],
                            'color': QColor(100, 255, 100),
                            'description': f'找到目标值: {value}'
                        })
                    elif not found and not is_insert:
                        steps.append({
                            'type': 'highlight',
                            'nodes': [node_id],
                            'color': QColor(255, 100, 100),
                            'description': f'未找到值: {value}'
                        })
                    else:
                        steps.append({
                            'type': 'highlight',
                            'nodes': [node_id],
                            'color': QColor(200, 200, 255),
                            'description': f'找到插入位置，{value} 将插入到节点 {node_value} 的{"左" if value < node_value else "右"}子树'
                        })
        else:
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(200, 200, 255),
                'description': f'树为空，{value} 将作为根节点插入'
            })
        
        return steps
    
    def _generate_huffman_steps(self, operation_type, data):
        """生成哈夫曼树操作的动画步骤"""
        steps = []
        
        if operation_type == 'huffman_build_from_text':
            text = data.get('text')
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(255, 200, 100),
                'description': f'分析文本: "{text}"'
            })
            steps.append({
                'type': 'execute',
                'action': 'build_from_text',
                'data': {'text': text},
                'description': f'构建哈夫曼树'
            })
            
        elif operation_type == 'huffman_build_from_frequency':
            frequency = data.get('frequency')
            steps.append({
                'type': 'highlight',
                'nodes': [],
                'color': QColor(255, 200, 100),
                'description': f'使用频率数据构建'
            })
            steps.append({
                'type': 'execute',
                'action': 'build_from_frequency',
                'data': {'frequency': frequency},
                'description': '构建哈夫曼树'
            })
            
        elif operation_type == 'huffman_encode':
            text = data.get('text')
            steps.append({
                'type': 'execute',
                'action': 'encode',
                'data': {'text': text},
                'description': f'编码文本: "{text}"'
            })
            
        elif operation_type == 'huffman_decode':
            code = data.get('code')
            steps.append({
                'type': 'execute',
                'action': 'decode',
                'data': {'code': code},
                'description': f'解码: {code}'
            })
            
        elif operation_type == 'huffman_clear':
            steps.append({
                'type': 'execute',
                'action': 'clear',
                'data': {},
                'description': '清空哈夫曼树'
            })
        
        return steps
    
    def play(self):
        """开始播放动画"""
        if not self.steps:
            QMessageBox.warning(self.main_window, "警告", "没有可播放的动画步骤")
            return
        
        if self.is_paused:
            self.is_paused = False
        else:
            self.current_step_index = 0
        
        self.is_playing = True
        self.timer.start(self.animation_speed)
        self.status_changed.emit("动画开始播放")
    
    def pause(self):
        """暂停动画"""
        self.is_playing = False
        self.is_paused = True
        self.timer.stop()
        self.status_changed.emit("动画已暂停")
    
    def stop(self):
        """停止动画"""
        self.is_playing = False
        self.is_paused = False
        self.timer.stop()
        self.current_step_index = 0
        self.status_changed.emit("动画已停止")
        self.animation_finished.emit()
    
    def next_step(self):
        """手动执行下一步"""
        if self.current_step_index < len(self.steps):
            self._execute_current_step()
            self.current_step_index += 1
            if self.current_step_index >= len(self.steps):
                self.stop()
    
    def previous_step(self):
        """执行上一步（需要重新执行到当前步骤）"""
        if self.current_step_index > 0:
            self.current_step_index -= 1
            # 这里需要重新构建数据结构到之前的状态
            # 简化实现：重新执行到当前步骤
            self.status_changed.emit("回退到上一步（功能待完善）")
    
    def _execute_next_step(self):
        """定时器触发的下一步执行"""
        if self.current_step_index < len(self.steps):
            self._execute_current_step()
            self.current_step_index += 1
            
            if self.current_step_index >= len(self.steps):
                self.stop()
            else:
                # 更新进度
                total = len(self.steps)
                current = self.current_step_index
                self.step_changed.emit(current, f"步骤 {current}/{total}")
    
    def _execute_current_step(self):
        """执行当前步骤"""
        if self.current_step_index >= len(self.steps):
            return
        
        step = self.steps[self.current_step_index]
        step_type = step.get('type')
        description = step.get('description', '')
        
        try:
            if step_type == 'highlight':
                # 高亮节点
                node_ids = step.get('nodes', [])
                color = step.get('color', QColor(255, 255, 0))
                self.highlight_requested.emit(node_ids, color, description)
                self.status_changed.emit(description)
                
            elif step_type == 'execute':
                # 执行实际操作前，先清除高亮
                self.highlight_requested.emit([], QColor(255, 255, 255), "")
                # 执行实际操作
                action = step.get('action')
                action_data = step.get('data', {})
                self._execute_operation(action, action_data)
                self.operation_executed.emit(description)
                self.status_changed.emit(description)
            
            # 更新显示
            self.main_window.update_display(description)
            
        except Exception as e:
            error_msg = f"执行步骤错误: {str(e)}"
            self.status_changed.emit(error_msg)
            print(error_msg)
    
    def _execute_operation(self, action, data):
        """执行具体的操作"""
        try:
            if action == 'insert_beginning':
                self.main_window.linked_list.insert_at_beginning(data['value'])
            elif action == 'insert_end':
                self.main_window.linked_list.insert_at_end(data['value'])
            elif action == 'insert_position':
                self.main_window.linked_list.insert_at_position(data['position'], data['value'])
            elif action == 'delete_position':
                self.main_window.linked_list.delete_at_position(data['position'])
            elif action == 'clear' and self.main_window.current_ds == "链表":
                self.main_window.linked_list.clear()
                
            elif action == 'push':
                self.main_window.stack.push(data['value'])
            elif action == 'pop':
                self.main_window.stack.pop()
            elif action == 'clear' and self.main_window.current_ds == "栈":
                self.main_window.stack = self.main_window.stack.__class__(10)
                
            elif action == 'enqueue':
                self.main_window.queue.enqueue(data['value'])
            elif action == 'dequeue':
                self.main_window.queue.dequeue()
            elif action == 'clear' and self.main_window.current_ds == "队列":
                self.main_window.queue = self.main_window.queue.__class__(10)
                
            elif action == 'insert_level_order':
                self.main_window.binary_tree.insert_level_order(data['value'])
            elif action == 'clear' and self.main_window.current_ds == "二叉树":
                self.main_window.binary_tree = self.main_window.binary_tree.__class__()
                
            elif action == 'insert':
                if self.main_window.current_ds == "二叉搜索树":
                    self.main_window.bst.insert(data['value'])
                    # 插入后高亮新节点
                    inserted_node = self.main_window.bst.search(data['value'])
                    if inserted_node and isinstance(inserted_node.data, dict):
                        node_id = inserted_node.data.get('id')
                        if node_id:
                            # 延迟高亮新节点（在下一个步骤中）
                            QTimer.singleShot(100, lambda: self.highlight_requested.emit(
                                [node_id], QColor(100, 255, 100), f'新节点 {data["value"]} 已插入'
                            ))
                elif self.main_window.current_ds == "AVL树":
                    self.main_window.avl_tree.insert(data['value'])
                    # 插入后高亮新节点
                    inserted_node = self.main_window.avl_tree.search(data['value'])
                    if inserted_node and isinstance(inserted_node.data, dict):
                        node_id = inserted_node.data.get('id')
                        if node_id:
                            QTimer.singleShot(100, lambda: self.highlight_requested.emit(
                                [node_id], QColor(100, 255, 100), f'新节点 {data["value"]} 已插入'
                            ))
            elif action == 'delete':
                if self.main_window.current_ds == "二叉搜索树":
                    self.main_window.bst.delete(data['value'])
                elif self.main_window.current_ds == "AVL树":
                    self.main_window.avl_tree.delete(data['value'])
            elif action == 'clear':
                if self.main_window.current_ds == "二叉搜索树":
                    self.main_window.bst.clear()
                elif self.main_window.current_ds == "AVL树":
                    self.main_window.avl_tree.clear()
                    
            elif action == 'build_from_text':
                self.main_window.huffman_tree.build_from_text(data['text'])
            elif action == 'build_from_frequency':
                self.main_window.huffman_tree.build_from_frequency(data['frequency'])
            elif action == 'encode':
                self.main_window.huffman_tree.encode(data['text'])
            elif action == 'decode':
                self.main_window.huffman_tree.decode(data['code'])
            elif action == 'clear' and self.main_window.current_ds == "哈夫曼树":
                self.main_window.huffman_tree = self.main_window.huffman_tree.__class__()
                
        except Exception as e:
            raise Exception(f"操作执行失败: {action}, 错误: {str(e)}")
    
    def clear_steps(self):
        """清空动画步骤队列"""
        self.steps = []
        self.current_step_index = 0
        self.stop()
        # 清除所有高亮
        self.highlight_requested.emit([], QColor(255, 255, 255), "")
        # 通知进度更新
        self.step_changed.emit(0, "操作队列已清空")
    
    def get_progress(self):
        """获取当前进度"""
        if not self.steps:
            return (0, 0)
        return (self.current_step_index, len(self.steps))

