from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from .graphics_view import GraphicsView
from .controls import ControlsPanel
from model.linked_list import LinkedList
from model.stack import Stack
from model.queue import Queue
from model.binary_tree import BinaryTree
from model.binary_search_tree import BinarySearchTree
from model.huffman_tree import HuffmanTree
from model.avl_tree import AVLTree
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
from utils.serializer import DataStructureSerializer
from view.file_dialog import FileDialog
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow  # 根据实际需要导入其他组件
from controller.animation_controller import AnimationController
from controller.unified_animation_controller import UnifiedAnimationController
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar,
                             QMenu, QAction, QMessageBox, QDialog, QApplication,
                             QGroupBox, QComboBox, QSlider, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from controller.algorithm_animator import AlgorithmAnimator


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.linked_list = LinkedList()
        self.stack = Stack()
        self.queue = Queue()
        self.binary_tree = BinaryTree()
        self.bst = BinarySearchTree()
        self.huffman_tree = HuffmanTree()
        self.avl_tree = AVLTree()  # 创建AVL树实例
        self.current_ds = "链表"
        self.init_ui()
        self.connect_signals()
        self.create_menus()
        # 添加统一动画控制器（新的动画系统）
        self.unified_animation_controller = UnifiedAnimationController(self)
        self.init_unified_animation_ui()
        self.connect_unified_animation_signals()
        # 添加动画控制器（保留旧系统以兼容）
        self.animation_controller = AnimationController(self)
        self.init_animation_ui()
        self.connect_animation_signals()
        # 添加算法动画控制器
        self.algorithm_animator = AlgorithmAnimator(self)
        self.init_algorithm_animation_ui()
        self.connect_algorithm_animation_signals()

    def create_menus(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        # 保存操作
        save_action = QAction('保存', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_data_structure)
        file_menu.addAction(save_action)

        # 加载操作
        load_action = QAction('加载', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(self.load_data_structure)
        file_menu.addAction(load_action)

        file_menu.addSeparator()

        # 退出操作
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def save_data_structure(self):
        """保存当前数据结构"""
        try:
            # 根据当前数据结构类型序列化数据
            serializer = DataStructureSerializer()
            data = None

            if self.current_ds == "链表":
                data = serializer.serialize_linked_list(self.linked_list)
            elif self.current_ds == "栈":
                data = serializer.serialize_stack(self.stack)
            elif self.current_ds == "队列":
                data = serializer.serialize_queue(self.queue)
            elif self.current_ds == "二叉树":
                data = serializer.serialize_binary_tree(self.binary_tree)
            elif self.current_ds == "二叉搜索树":
                data = serializer.serialize_bst(self.bst)
            elif self.current_ds == "哈夫曼树":
                data = serializer.serialize_huffman(self.huffman_tree)
            elif self.current_ds == "AVL树":
                data = serializer.serialize_avl(self.avl_tree)
            else:
                QMessageBox.warning(self, "保存失败", f"不支持保存 {self.current_ds} 类型")
                return

            # 显示保存对话框
            dialog = FileDialog(self, mode="save")
            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.get_selected_file()
                if filename:
                    serializer.save_to_file(data, filename)
                    self.status_bar.showMessage(f"数据结构已保存到: {filename}")
                else:
                    self.status_bar.showMessage("保存取消")
            else:
                self.status_bar.showMessage("保存取消")

        except Exception as e:
            QMessageBox.critical(self, "保存错误", f"保存失败: {str(e)}")

    def load_data_structure(self):
        """加载数据结构"""
        try:
            # 显示加载对话框
            dialog = FileDialog(self, mode="load")
            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.get_selected_file()
                if filename:
                    # 从文件加载数据
                    loaded_data = DataStructureSerializer.load_from_file(filename)
                    data_type = loaded_data.get("type")

                    # 根据类型反序列化
                    serializer = DataStructureSerializer()

                    if data_type == "LinkedList":
                        self.linked_list = serializer.deserialize_linked_list(loaded_data["data"])
                        self.current_ds = "链表"
                    elif data_type == "Stack":
                        self.stack = serializer.deserialize_stack(loaded_data)
                        self.current_ds = "栈"
                    elif data_type == "Queue":
                        self.queue = serializer.deserialize_queue(loaded_data)
                        self.current_ds = "队列"
                    elif data_type == "BinaryTree":
                        self.binary_tree = serializer.deserialize_binary_tree(loaded_data)
                        self.current_ds = "二叉树"
                    elif data_type == "BinarySearchTree":
                        self.bst = serializer.deserialize_bst(loaded_data)
                        self.current_ds = "二叉搜索树"
                    elif data_type == "HuffmanTree":
                        self.huffman_tree = serializer.deserialize_huffman(loaded_data)
                        self.current_ds = "哈夫曼树"
                    elif data_type == "AVLTree":
                        self.avl_tree = serializer.deserialize_avl(loaded_data)
                        self.current_ds = "AVL树"
                    else:
                        QMessageBox.warning(self, "加载失败", f"未知的数据结构类型: {data_type}")
                        return

                    # 更新界面
                    self.controls_panel.ds_combo.setCurrentText(self.current_ds)
                    self.update_display(f"已加载: {filename}")

                else:
                    self.status_bar.showMessage("加载取消")
            else:
                self.status_bar.showMessage("加载取消")

        except Exception as e:
            QMessageBox.critical(self, "加载错误", f"加载失败: {str(e)}")

    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>数据结构可视化模拟器</h2>
        <p>版本 1.0</p>
        <p>一个用于学习和演示数据结构的可视化工具。</p>
        <p><b>支持的数据结构:</b></p>
        <ul>
            <li>链表（顺序表、链表）</li>
            <li>栈（顺序栈）</li>
            <li>队列</li>
            <li>二叉树</li>
            <li>二叉搜索树（BST）</li>
            <li>哈夫曼树</li>
            <li>AVL树（平衡二叉搜索树）</li>
        </ul>
        <p><b>功能特性:</b></p>
        <ul>
            <li>动态可视化数据结构操作</li>
            <li>支持文件保存和加载</li>
            <li>指令系统支持</li>
            <li>良好的用户界面</li>
        </ul>
        <p>开发基于 PyQt5 框架。</p>
        """

        QMessageBox.about(self, "关于", about_text)

    def init_ui(self):
        self.setWindowTitle("数据结构可视化模拟器")
        self.setGeometry(100, 100, 1200, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QHBoxLayout(central_widget)

        # 左侧控制面板
        self.controls_panel = ControlsPanel()
        main_layout.addWidget(self.controls_panel, 1)  # 1份宽度

        # 右侧图形视图
        self.graphics_view = GraphicsView()
        main_layout.addWidget(self.graphics_view, 3)  # 3份宽度

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 初始绘制
        self.update_display()

    def connect_signals(self):
        """连接信号和槽"""
        # 连接文件操作
        self.controls_panel.connect_file_signals(
            self.save_data_structure,
            self.load_data_structure,
            self.show_about
        )
        # 连接链表操作
        self.controls_panel.connect_ll_signals(
            self.insert_beginning,
            self.insert_end,
            self.insert_at_position,
            self.delete_at_position,
            self.clear_list
        )

        # 连接栈操作
        self.controls_panel.connect_stack_signals(
            self.push,
            self.pop,
            self.clear_stack
        )

        # 连接队列操作
        self.controls_panel.connect_queue_signals(
            self.enqueue,
            self.dequeue,
            self.clear_queue
        )

        # 连接二叉树操作
        self.controls_panel.connect_binary_tree_signals(
            self.binary_tree_insert_level,
            self.clear_binary_tree,
            self.binary_tree_batch_insert
        )

        # 连接二叉搜索树操作
        self.controls_panel.connect_bst_signals(
            self.bst_insert,
            self.bst_search,
            self.bst_delete,
            self.clear_bst,
            self.bst_batch_insert
        )

        # 连接哈夫曼树操作
        self.controls_panel.connect_huffman_signals(
            self.huffman_build_from_text,
            self.huffman_build_from_frequency,
            self.huffman_encode,
            self.huffman_decode,
            self.clear_huffman
        )

        # 连接AVL树操作
        self.controls_panel.connect_avl_signals(
            self.avl_insert,
            self.avl_search,
            self.avl_delete,
            self.clear_avl,
            self.avl_batch_insert
        )

        # 连接数据结构选择
        self.controls_panel.ds_combo.currentTextChanged.connect(self.on_ds_selected)

        # 连接指令执行
        self.controls_panel.execute_cmd_btn.clicked.connect(self.execute_command)

    def on_ds_selected(self, ds_name):
        """当选择不同的数据结构时"""
        self.current_ds = ds_name
        self.update_display(f"切换到: {ds_name}")

    # 链表操作方法
    def insert_beginning(self):
        """在链表开头插入节点"""
        value = self.controls_panel.get_value()
        # 使用动画控制器 - 只添加步骤，不自动播放
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'linked_list_insert_beginning',
                {'value': value}
            )
            # 不自动播放，让用户手动控制
            self.status_bar.showMessage(f"已添加插入操作，请使用'下一步'按钮单步执行")
        else:
            # 兼容模式：立即执行
            self.linked_list.insert_at_beginning(value)
            self.update_display(f"在开头插入节点: {value}")

    def insert_end(self):
        """在链表末尾插入节点"""
        value = self.controls_panel.get_value()
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'linked_list_insert_end',
                {'value': value}
            )
            self.status_bar.showMessage(f"已添加插入操作，请使用'下一步'按钮单步执行")
        else:
            self.linked_list.insert_at_end(value)
            self.update_display(f"在末尾插入节点: {value}")

    def insert_at_position(self):
        """在指定位置插入节点"""
        value = self.controls_panel.get_value()
        position = self.controls_panel.get_position()

        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'linked_list_insert_position',
                    {'value': value, 'position': position}
                )
                self.status_bar.showMessage(f"已添加插入操作，请使用'下一步'按钮单步执行")
            else:
                self.linked_list.insert_at_position(position, value)
                self.update_display(f"在位置 {position} 插入节点: {value}")
        except IndexError as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def delete_at_position(self):
        """删除指定位置的节点"""
        position = self.controls_panel.get_position()

        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'linked_list_delete_position',
                    {'position': position}
                )
                self.status_bar.showMessage(f"已添加删除操作，请使用'下一步'按钮单步执行")
            else:
                deleted_node = self.linked_list.delete_at_position(position)
                self.update_display(f"删除位置 {position} 的节点: {deleted_node.data}")
        except IndexError as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_list(self):
        """清空链表"""
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'linked_list_clear',
                {}
            )
            self.status_bar.showMessage(f"已添加清空操作，请使用'下一步'按钮单步执行")
        else:
            self.linked_list.clear()
            self.update_display("链表已清空")

    # 栈操作方法
    def push(self):
        """入栈操作"""
        value = self.controls_panel.stack_value_spin.value()
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'stack_push',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加入栈操作，请使用'下一步'按钮单步执行")
            else:
                self.stack.push(value)
                self.update_display(f"入栈: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def pop(self):
        """出栈操作"""
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'stack_pop',
                    {}
                )
                self.status_bar.showMessage(f"已添加出栈操作，请使用'下一步'按钮单步执行")
            else:
                value = self.stack.pop()
                self.update_display(f"出栈: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_stack(self):
        """清空栈"""
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'stack_clear',
                {}
            )
            self.status_bar.showMessage(f"已添加清空操作，请使用'下一步'按钮单步执行")
        else:
            self.stack = Stack()
            self.update_display("栈已清空")

    # 队列操作方法
    def enqueue(self):
        """入队操作"""
        value = self.controls_panel.queue_value_spin.value()
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'queue_enqueue',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加入队操作，请使用'下一步'按钮单步执行")
            else:
                self.queue.enqueue(value)
                self.update_display(f"入队: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def dequeue(self):
        """出队操作"""
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'queue_dequeue',
                    {}
                )
                self.status_bar.showMessage(f"已添加出队操作，请使用'下一步'按钮单步执行")
            else:
                value = self.queue.dequeue()
                self.update_display(f"出队: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_queue(self):
        """清空队列"""
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'queue_clear',
                {}
            )
            self.status_bar.showMessage(f"已添加清空操作，请使用'下一步'按钮单步执行")
        else:
            self.queue = Queue()
            self.update_display("队列已清空")

    # 二叉树操作方法

    def binary_tree_insert_level(self):
        """二叉树层次插入"""
        value = self.controls_panel.bt_value_spin.value()

        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'binary_tree_insert',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加插入操作，请使用'下一步'按钮单步执行")
            else:
                success = self.binary_tree.insert_level_order(value)
                if success:
                    self.update_display(f"二叉树层次插入: {value}")
                else:
                    self.status_bar.showMessage("错误: 无法插入节点")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def binary_tree_batch_insert(self):
        """二叉树批量插入"""
        values = self.controls_panel.get_binary_tree_batch_values()
        if not values:
            self.status_bar.showMessage("错误: 请输入有效的数值")
            return

        try:
            self.binary_tree.insert_level_order_batch(values)
            self.update_display(f"二叉树批量插入: {', '.join(map(str, values))}")
            self.controls_panel.clear_binary_tree_batch_input()
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_binary_tree(self):
        """清空二叉树"""
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'binary_tree_clear',
                {}
            )
            self.status_bar.showMessage(f"已添加清空操作，请使用'下一步'按钮单步执行")
        else:
            self.binary_tree = BinaryTree()
            self.update_display("二叉树已清空")

    # 二叉搜索树操作方法
    def bst_insert(self):
        """BST插入"""
        value = self.controls_panel.bst_value_spin.value()
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'bst_insert',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加插入操作，请使用'下一步'按钮单步执行")
            else:
                self.bst.insert(value)
                self.update_display(f"BST插入: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def bst_search(self):
        """BST查找"""
        value = self.controls_panel.bst_value_spin.value()
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'bst_search',
                {'value': value}
            )
            self.status_bar.showMessage(f"已添加查找操作，请使用'下一步'按钮单步执行")
        else:
            node = self.bst.search(value)
            if node:
                self.update_display(f"BST查找: 找到 {value}")
            else:
                self.update_display(f"BST查找: 未找到 {value}")

    def bst_delete(self):
        """BST删除"""
        value = self.controls_panel.bst_value_spin.value()
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'bst_delete',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加删除操作，请使用'下一步'按钮单步执行")
            else:
                self.bst.delete(value)
                self.update_display(f"BST删除: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def bst_batch_insert(self):
        """BST批量插入"""
        values = self.controls_panel.get_bst_batch_values()
        if not values:
            self.status_bar.showMessage("错误: 请输入有效的数值")
            return

        for value in values:
            self.bst.insert(value)

        self.update_display(f"BST批量插入: {', '.join(map(str, values))}")
        self.controls_panel.clear_bst_batch_input()

    def clear_bst(self):
        """清空BST"""
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'bst_clear',
                {}
            )
            self.status_bar.showMessage(f"已添加清空操作，请使用'下一步'按钮单步执行")
        else:
            self.bst = BinarySearchTree()
            self.update_display("二叉搜索树已清空")

    # 哈夫曼树操作方法
    def huffman_build_from_text(self):
        """从文本构建哈夫曼树"""
        text = self.controls_panel.get_huffman_text()
        if not text:
            self.status_bar.showMessage("错误: 请输入文本")
            return

        try:
            self.huffman_tree.build_from_text(text)
            self.update_display(f"哈夫曼树构建完成: '{text}'")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def huffman_build_from_frequency(self):
        """从频率构建哈夫曼树"""
        frequency = self.controls_panel.get_huffman_frequency()
        if not frequency:
            self.status_bar.showMessage("错误: 请输入有效的频率数据")
            return

        try:
            self.huffman_tree.build_from_frequency(frequency)
            self.update_display(f"哈夫曼树构建完成: {frequency}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def huffman_encode(self):
        """哈夫曼编码"""
        text = self.controls_panel.get_huffman_text()
        if not text:
            self.status_bar.showMessage("错误: 请输入要编码的文本")
            return

        try:
            encoded = self.huffman_tree.encode(text)
            self.update_display(f"编码结果: {encoded}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def huffman_decode(self):
        """哈夫曼解码"""
        # 这里需要获取编码文本，简化实现，使用输入框中的文本
        text = self.controls_panel.get_huffman_text()
        if not text:
            self.status_bar.showMessage("错误: 请输入要解码的二进制串")
            return

        try:
            # 验证输入是否为二进制
            if any(c not in '01' for c in text):
                self.status_bar.showMessage("错误: 解码输入必须是二进制串(只包含0和1)")
                return

            decoded = self.huffman_tree.decode(text)
            self.update_display(f"解码结果: '{decoded}'")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_huffman(self):
        """清空哈夫曼树"""
        self.huffman_tree = HuffmanTree()
        self.update_display("哈夫曼树已清空")

    # AVL树操作方法
    def avl_insert(self):
        """AVL插入"""
        value = self.controls_panel.avl_value_spin.value()
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'avl_insert',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加插入操作，请使用'下一步'按钮单步执行")
            else:
                self.avl_tree.insert(value)
                self.update_display(f"AVL插入: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def avl_search(self):
        """AVL查找"""
        value = self.controls_panel.avl_value_spin.value()
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'avl_search',
                {'value': value}
            )
            self.status_bar.showMessage(f"已添加查找操作，请使用'下一步'按钮单步执行")
        else:
            node = self.avl_tree.search(value)
            if node:
                self.update_display(f"AVL查找: 找到 {value}")
            else:
                self.update_display(f"AVL查找: 未找到 {value}")

    def avl_delete(self):
        """AVL删除"""
        value = self.controls_panel.avl_value_spin.value()
        try:
            if hasattr(self, 'unified_animation_controller'):
                self.unified_animation_controller.add_operation(
                    'avl_delete',
                    {'value': value}
                )
                self.status_bar.showMessage(f"已添加删除操作，请使用'下一步'按钮单步执行")
            else:
                self.avl_tree.delete(value)
                self.update_display(f"AVL删除: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def avl_batch_insert(self):
        """AVL批量插入"""
        values = self.controls_panel.get_avl_batch_values()
        if not values:
            self.status_bar.showMessage("错误: 请输入有效的数值")
            return

        for value in values:
            self.avl_tree.insert(value)

        self.update_display(f"AVL批量插入: {', '.join(map(str, values))}")
        self.controls_panel.clear_avl_batch_input()

    def clear_avl(self):
        """清空AVL树"""
        if hasattr(self, 'unified_animation_controller'):
            self.unified_animation_controller.add_operation(
                'avl_clear',
                {}
            )
            self.status_bar.showMessage(f"已添加清空操作，请使用'下一步'按钮单步执行")
        else:
            self.avl_tree = AVLTree()
            self.update_display("AVL树已清空")

    def update_display(self, message=None):
        """更新显示"""
        if message:
            self.status_bar.showMessage(message)
            if hasattr(self, 'graphics_view'):
                self.graphics_view.add_operation_text(message)

        if not hasattr(self, 'graphics_view'):
            return

        # 根据当前选择的数据结构调用对应的绘制方法
        if self.current_ds == "链表":
            if self.linked_list.head is not None:
                self.graphics_view.draw_linked_list(self.linked_list)
            else:
                self.graphics_view.clear_scene()
        elif self.current_ds == "栈":
            self.graphics_view.draw_stack(self.stack)
        elif self.current_ds == "队列":
            self.graphics_view.draw_queue(self.queue)
        elif self.current_ds == "二叉树":
            self.graphics_view.draw_binary_tree(self.binary_tree)
        elif self.current_ds == "二叉搜索树":
            self.graphics_view.draw_binary_search_tree(self.bst)
        elif self.current_ds == "哈夫曼树":
            self.graphics_view.draw_huffman_tree(self.huffman_tree)
        elif self.current_ds == "AVL树":
            self.graphics_view.draw_avl_tree(self.avl_tree)

    def execute_command(self):
        """执行指令"""
        command = self.controls_panel.get_command()
        if not command:
            return

        # 简化版指令解析
        parts = command.lower().split()

        try:
            # 链表指令
            if len(parts) >= 2 and parts[0] == "insert":
                value = int(parts[1])
                if "beginning" in command:
                    self.linked_list.insert_at_beginning(value)
                    self.update_display(f"指令执行: {command}")
                elif "end" in command:
                    self.linked_list.insert_at_end(value)
                    self.update_display(f"指令执行: {command}")
                elif "at" in command and len(parts) > 3:
                    position = int(parts[3])
                    self.linked_list.insert_at_position(position, value)
                    self.update_display(f"指令执行: {command}")

            # 栈指令
            elif parts[0] == "push" and len(parts) > 1:
                value = int(parts[1])
                self.stack.push(value)
                self.update_display(f"指令执行: {command}")

            elif parts[0] == "pop":
                value = self.stack.pop()
                self.update_display(f"指令执行: {command}, 出栈: {value}")

            # 队列指令
            elif parts[0] == "enqueue" and len(parts) > 1:
                value = int(parts[1])
                self.queue.enqueue(value)
                self.update_display(f"指令执行: {command}")

            elif parts[0] == "dequeue":
                value = self.queue.dequeue()
                self.update_display(f"指令执行: {command}, 出队: {value}")

            # 二叉树指令
            elif parts[0] == "bt_insert" and len(parts) > 1:
                value = int(parts[1])
                success = self.binary_tree.insert_level_order(value)
                if success:
                    self.update_display(f"指令执行: {command}")
                else:
                    self.status_bar.showMessage(f"指令执行失败: {command}")

            # 二叉搜索树指令
            elif parts[0] == "bst_insert" and len(parts) > 1:
                value = int(parts[1])
                self.bst.insert(value)
                self.update_display(f"指令执行: {command}")

            elif parts[0] == "bst_search" and len(parts) > 1:
                value = int(parts[1])
                node = self.bst.search(value)
                if node:
                    self.update_display(f"指令执行: {command}, 找到 {value}")
                else:
                    self.update_display(f"指令执行: {command}, 未找到 {value}")

            elif parts[0] == "bst_delete" and len(parts) > 1:
                value = int(parts[1])
                self.bst.delete(value)
                self.update_display(f"指令执行: {command}")

            # 哈夫曼树指令
            elif parts[0] == "huffman_build" and len(parts) > 1:
                # 提取文本（可能包含空格）
                text = command[len("huffman_build"):].strip().strip("'\"")
                self.huffman_tree.build_from_text(text)
                self.update_display(f"指令执行: {command}")

            # AVL树指令
            elif parts[0] == "avl_insert" and len(parts) > 1:
                value = int(parts[1])
                self.avl_tree.insert(value)
                self.update_display(f"指令执行: {command}")

            elif parts[0] == "avl_search" and len(parts) > 1:
                value = int(parts[1])
                node = self.avl_tree.search(value)
                if node:
                    self.update_display(f"指令执行: {command}, 找到 {value}")
                else:
                    self.update_display(f"指令执行: {command}, 未找到 {value}")

            elif parts[0] == "avl_delete" and len(parts) > 1:
                value = int(parts[1])
                self.avl_tree.delete(value)
                self.update_display(f"指令执行: {command}")

            elif len(parts) >= 2 and parts[0] == "delete":
                if "position" in command and len(parts) > 2:
                    position = int(parts[2])
                    deleted_node = self.linked_list.delete_at_position(position)
                    self.update_display(f"指令执行: {command}")

            elif command == "clear":
                if self.current_ds == "链表":
                    self.linked_list.clear()
                    self.update_display("指令执行: 清空链表")
                elif self.current_ds == "栈":
                    self.stack = Stack()
                    self.update_display("指令执行: 清空栈")
                elif self.current_ds == "队列":
                    self.queue = Queue()
                    self.update_display("指令执行: 清空队列")
                elif self.current_ds == "二叉树":
                    self.binary_tree = BinaryTree()
                    self.update_display("指令执行: 清空二叉树")
                elif self.current_ds == "二叉搜索树":
                    self.bst = BinarySearchTree()
                    self.update_display("指令执行: 清空二叉搜索树")
                elif self.current_ds == "哈夫曼树":
                    self.huffman_tree = HuffmanTree()
                    self.update_display("指令执行: 清空哈夫曼树")
                elif self.current_ds == "AVL树":
                    self.avl_tree = AVLTree()
                    self.update_display("指令执行: 清空AVL树")

            else:
                self.status_bar.showMessage(f"未知指令: {command}")

        except (ValueError, IndexError, Exception) as e:
            self.status_bar.showMessage(f"指令错误: {str(e)}")

        self.controls_panel.clear_command()

    def init_animation_ui(self):
        """初始化动画演示界面"""
        # 在控制面板中添加动画演示区域
        if hasattr(self.controls_panel, 'layout'):
            # 创建动画演示组
            animation_group = QGroupBox("动画演示")
            animation_layout = QVBoxLayout()

            # 演示选择
            demo_layout = QHBoxLayout()
            demo_layout.addWidget(QLabel("选择演示:"))
            self.demo_combo = QComboBox()
            self.demo_combo.addItems([
                "链表基本操作",
                "栈的LIFO特性",
                "队列的FIFO特性",
                "二叉搜索树构建",
                "AVL树平衡演示",
                "哈夫曼编码"
            ])
            demo_layout.addWidget(self.demo_combo)
            demo_layout.addStretch()

            # 速度控制
            speed_layout = QHBoxLayout()
            speed_layout.addWidget(QLabel("速度:"))
            self.speed_slider = QSlider(Qt.Horizontal)
            self.speed_slider.setRange(100, 3000)
            self.speed_slider.setValue(1000)
            self.speed_slider.setTickPosition(QSlider.TicksBelow)
            self.speed_slider.setTickInterval(500)
            speed_layout.addWidget(self.speed_slider)
            self.speed_label = QLabel("1.0s")
            speed_layout.addWidget(self.speed_label)

            # 控制按钮
            button_layout = QHBoxLayout()
            self.load_demo_btn = QPushButton("加载演示")
            self.play_btn = QPushButton("播放")
            self.pause_btn = QPushButton("暂停")
            self.stop_btn = QPushButton("停止")
            self.prev_btn = QPushButton("上一步")
            self.next_btn = QPushButton("下一步")

            button_layout.addWidget(self.load_demo_btn)
            button_layout.addWidget(self.play_btn)
            button_layout.addWidget(self.pause_btn)
            button_layout.addWidget(self.stop_btn)
            button_layout.addWidget(self.prev_btn)
            button_layout.addWidget(self.next_btn)

            # 进度显示
            progress_layout = QHBoxLayout()
            progress_layout.addWidget(QLabel("进度:"))
            self.progress_label = QLabel("0/0")
            self.step_description = QLabel("请选择演示内容")
            self.step_description.setWordWrap(True)

            progress_layout.addWidget(self.progress_label)
            progress_layout.addStretch()

            animation_layout.addLayout(demo_layout)
            animation_layout.addLayout(speed_layout)
            animation_layout.addLayout(button_layout)
            animation_layout.addLayout(progress_layout)
            animation_layout.addWidget(self.step_description)

            animation_group.setLayout(animation_layout)

            # 添加到控制面板
            self.controls_panel.layout().insertWidget(2, animation_group)  # 插入到第三个位置

    def connect_animation_signals(self):
        """连接动画信号"""
        # 按钮信号
        self.load_demo_btn.clicked.connect(self.load_demo)
        self.play_btn.clicked.connect(self.animation_controller.play)
        self.pause_btn.clicked.connect(self.animation_controller.pause)
        self.stop_btn.clicked.connect(self.animation_controller.stop)
        self.prev_btn.clicked.connect(self.animation_controller.previous_step)
        self.next_btn.clicked.connect(self.animation_controller.next_step)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)

        # 动画控制器信号
        self.animation_controller.status_changed.connect(self.on_animation_status_changed)
        self.animation_controller.step_changed.connect(self.on_animation_step_changed)
        self.animation_controller.animation_finished.connect(self.on_animation_finished)

    def load_demo(self):
        """加载演示"""
        demo_name = self.demo_combo.currentText()
        step_count = self.animation_controller.load_demo(demo_name)
        self.progress_label.setText(f"0/{step_count}")
        self.step_description.setText(f"已加载演示: {demo_name}")

        # 根据演示类型切换数据结构
        if '链表' in demo_name:
            self.current_ds = "链表"
            self.controls_panel.ds_combo.setCurrentText("链表")
        elif '栈' in demo_name:
            self.current_ds = "栈"
            self.controls_panel.ds_combo.setCurrentText("栈")
        elif '队列' in demo_name:
            self.current_ds = "队列"
            self.controls_panel.ds_combo.setCurrentText("队列")
        elif '二叉搜索树' in demo_name:
            self.current_ds = "二叉搜索树"
            self.controls_panel.ds_combo.setCurrentText("二叉搜索树")
        elif 'AVL树' in demo_name:
            self.current_ds = "AVL树"
            self.controls_panel.ds_combo.setCurrentText("AVL树")
        elif '哈夫曼树' in demo_name:
            self.current_ds = "哈夫曼树"
            self.controls_panel.ds_combo.setCurrentText("哈夫曼树")

    def on_speed_changed(self, value):
        """速度改变"""
        speed_sec = value / 1000.0
        self.speed_label.setText(f"{speed_sec:.1f}s")
        self.animation_controller.set_animation_speed(value)

    def on_animation_status_changed(self, status):
        """动画状态改变"""
        self.status_bar.showMessage(status)

    def on_animation_step_changed(self, step, description):
        """动画步骤改变"""
        total_steps = len(self.animation_controller.steps)
        self.progress_label.setText(f"{step}/{total_steps}")
        self.step_description.setText(description)

    def on_animation_finished(self):
        """动画完成"""
        self.progress_label.setText("演示完成")
        self.step_description.setText("动画演示已结束")

    def init_algorithm_animation_ui(self):
        """初始化算法动画界面"""
        # 在控制面板中添加算法动画区域
        if hasattr(self.controls_panel, 'layout'):
            # 创建算法动画组
            algo_group = QGroupBox("算法动画演示")
            algo_layout = QVBoxLayout()

            # 算法选择
            algo_select_layout = QHBoxLayout()
            algo_select_layout.addWidget(QLabel("选择算法:"))
            self.algo_combo = QComboBox()
            self.algo_combo.addItems([
                "二叉搜索树查找",
                "哈夫曼树构建",
                "AVL树插入",
                "AVL树删除"
            ])
            algo_select_layout.addWidget(self.algo_combo)

            # 参数输入
            param_layout = QHBoxLayout()
            param_layout.addWidget(QLabel("参数:"))
            self.algo_param_input = QLineEdit()
            self.algo_param_input.setPlaceholderText("如: 50 或 ABRACADABRA")
            param_layout.addWidget(self.algo_param_input)

            # 速度控制
            speed_layout = QHBoxLayout()
            speed_layout.addWidget(QLabel("速度:"))
            self.algo_speed_slider = QSlider(Qt.Horizontal)
            self.algo_speed_slider.setRange(500, 3000)
            self.algo_speed_slider.setValue(1000)
            speed_layout.addWidget(self.algo_speed_slider)
            self.algo_speed_label = QLabel("1.0s")
            speed_layout.addWidget(self.algo_speed_label)

            # 控制按钮
            # 在控制按钮布局中添加测试按钮
            control_layout = QHBoxLayout()
            self.start_algo_btn = QPushButton("开始演示")
            self.pause_algo_btn = QPushButton("暂停")
            self.stop_algo_btn = QPushButton("停止")
            self.step_algo_btn = QPushButton("单步执行")
            self.test_algo_btn = QPushButton("测试动画")  # 添加测试按钮

            control_layout.addWidget(self.start_algo_btn)
            control_layout.addWidget(self.pause_algo_btn)
            control_layout.addWidget(self.stop_algo_btn)
            control_layout.addWidget(self.step_algo_btn)
            control_layout.addWidget(self.test_algo_btn)

            # 进度和状态显示
            status_layout = QVBoxLayout()
            self.algo_progress_label = QLabel("准备就绪")
            self.algo_step_description = QLabel("请选择算法并设置参数")
            self.algo_step_description.setWordWrap(True)
            self.algo_step_description.setStyleSheet("background-color: #f0f0f0; padding: 5px;")

            status_layout.addWidget(self.algo_progress_label)
            status_layout.addWidget(self.algo_step_description)

            algo_layout.addLayout(algo_select_layout)
            algo_layout.addLayout(param_layout)
            algo_layout.addLayout(speed_layout)
            algo_layout.addLayout(control_layout)
            algo_layout.addLayout(status_layout)

            algo_group.setLayout(algo_layout)

            # 添加到控制面板
            self.controls_panel.layout().insertWidget(2, algo_group)

    def connect_algorithm_animation_signals(self):
        """连接算法动画信号"""
        # 按钮信号
        self.start_algo_btn.clicked.connect(self.start_algorithm_demo)
        self.pause_algo_btn.clicked.connect(self.algorithm_animator.pause_algorithm)
        self.stop_algo_btn.clicked.connect(self.algorithm_animator.stop_algorithm)
        self.step_algo_btn.clicked.connect(self.algorithm_animator.execute_next_step)
        self.algo_speed_slider.valueChanged.connect(self.on_algo_speed_changed)

        # 算法动画控制器信号
        self.algorithm_animator.step_started.connect(self.on_algorithm_step_started)
        self.algorithm_animator.step_finished.connect(self.on_algorithm_step_finished)
        self.algorithm_animator.algorithm_finished.connect(self.on_algorithm_finished)
        self.algorithm_animator.highlight_nodes.connect(self.graphics_view.highlight_nodes)

        # 添加测试按钮连接
        self.test_algo_btn.clicked.connect(self.test_animation)

    def start_algorithm_demo(self):
        """开始算法演示"""
        algorithm_name = self.algo_combo.currentText()
        param_text = self.algo_param_input.text().strip()

        # 解析参数
        data = {}
        if algorithm_name == "二叉搜索树查找":
            try:
                data['value'] = int(param_text) if param_text else 50
            except ValueError:
                QMessageBox.warning(self, "参数错误", "请输入有效的整数值")
                return
        elif algorithm_name == "哈夫曼树构建":
            data['text'] = param_text if param_text else "ABRACADABRA"
        elif algorithm_name == "AVL树插入":
            try:
                if param_text:
                    data['values'] = [int(x.strip()) for x in param_text.split(',')]
                else:
                    data['values'] = [10, 20, 30, 40, 50]
            except ValueError:
                QMessageBox.warning(self, "参数错误", "请输入有效的整数值，用逗号分隔")
                return
        elif algorithm_name == "AVL树删除":
            try:
                data['value'] = int(param_text) if param_text else 20
            except ValueError:
                QMessageBox.warning(self, "参数错误", "请输入有效的整数值")
                return

        # 确保选择正确的数据结构
        if "二叉搜索树" in algorithm_name:
            self.current_ds = "二叉搜索树"
            self.controls_panel.ds_combo.setCurrentText("二叉搜索树")
        elif "哈夫曼树" in algorithm_name:
            self.current_ds = "哈夫曼树"
            self.controls_panel.ds_combo.setCurrentText("哈夫曼树")
        elif "AVL树" in algorithm_name:
            self.current_ds = "AVL树"
            self.controls_panel.ds_combo.setCurrentText("AVL树")

        # 开始算法演示
        self.algorithm_animator.start_algorithm(algorithm_name, data)
        self.algo_progress_label.setText(f"正在演示: {algorithm_name}")

    def on_algo_speed_changed(self, value):
        """算法速度改变"""
        speed_sec = value / 1000.0
        self.algo_speed_label.setText(f"{speed_sec:.1f}s")
        self.algorithm_animator.set_speed(value)

    def on_algorithm_step_started(self, step_index, description):
        """算法步骤开始"""
        self.algo_step_description.setText(description)
        self.status_bar.showMessage(f"步骤 {step_index + 1}: {description}")

    def on_algorithm_step_finished(self, step_index, description):
        """算法步骤完成"""
        # 可以在这里添加步骤完成后的处理
        pass

    def on_algorithm_finished(self, algorithm_name):
        """算法完成"""
        self.algo_progress_label.setText("演示完成")
        self.algo_step_description.setText(f"{algorithm_name} 演示已结束")
        self.status_bar.showMessage(f"{algorithm_name} 演示完成")

    def init_unified_animation_ui(self):
        """初始化统一动画控制UI"""
        # 在控制面板中添加统一动画控制区域
        if hasattr(self.controls_panel, 'layout'):
            # 创建统一动画控制组
            unified_anim_group = QGroupBox("动画控制")
            unified_anim_layout = QVBoxLayout()
            
            # 速度控制
            speed_layout = QHBoxLayout()
            speed_layout.addWidget(QLabel("速度:"))
            self.unified_speed_slider = QSlider(Qt.Horizontal)
            self.unified_speed_slider.setRange(200, 3000)
            self.unified_speed_slider.setValue(1000)
            self.unified_speed_slider.setTickPosition(QSlider.TicksBelow)
            self.unified_speed_slider.setTickInterval(500)
            speed_layout.addWidget(self.unified_speed_slider)
            self.unified_speed_label = QLabel("1.0s")
            speed_layout.addWidget(self.unified_speed_label)
            
            # 控制按钮
            button_layout = QHBoxLayout()
            self.unified_play_btn = QPushButton("播放")
            self.unified_pause_btn = QPushButton("暂停")
            self.unified_stop_btn = QPushButton("停止")
            self.unified_prev_btn = QPushButton("上一步")
            self.unified_next_btn = QPushButton("下一步")
            
            button_layout.addWidget(self.unified_play_btn)
            button_layout.addWidget(self.unified_pause_btn)
            button_layout.addWidget(self.unified_stop_btn)
            button_layout.addWidget(self.unified_prev_btn)
            button_layout.addWidget(self.unified_next_btn)
            
            # 进度显示
            progress_layout = QHBoxLayout()
            progress_layout.addWidget(QLabel("进度:"))
            self.unified_progress_label = QLabel("0/0")
            progress_layout.addWidget(self.unified_progress_label)
            progress_layout.addStretch()
            
            # 步骤描述
            self.unified_step_description = QLabel("准备就绪")
            self.unified_step_description.setWordWrap(True)
            self.unified_step_description.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
            
            unified_anim_layout.addLayout(speed_layout)
            unified_anim_layout.addLayout(button_layout)
            unified_anim_layout.addLayout(progress_layout)
            unified_anim_layout.addWidget(self.unified_step_description)
            
            unified_anim_group.setLayout(unified_anim_layout)
            
            # 添加到控制面板（插入到第一个位置）
            self.controls_panel.layout().insertWidget(1, unified_anim_group)
    
    def connect_unified_animation_signals(self):
        """连接统一动画控制信号"""
        # 按钮信号
        self.unified_play_btn.clicked.connect(self.unified_animation_controller.play)
        self.unified_pause_btn.clicked.connect(self.unified_animation_controller.pause)
        self.unified_stop_btn.clicked.connect(self.unified_animation_controller.stop)
        self.unified_prev_btn.clicked.connect(self.unified_animation_controller.previous_step)
        self.unified_next_btn.clicked.connect(self.unified_animation_controller.next_step)
        self.unified_speed_slider.valueChanged.connect(self.on_unified_speed_changed)
        
        # 动画控制器信号
        self.unified_animation_controller.step_changed.connect(self.on_unified_step_changed)
        self.unified_animation_controller.animation_finished.connect(self.on_unified_animation_finished)
        self.unified_animation_controller.status_changed.connect(self.on_unified_status_changed)
        self.unified_animation_controller.highlight_requested.connect(self.graphics_view.highlight_nodes)
    
    def on_unified_speed_changed(self, value):
        """统一动画速度改变"""
        speed_sec = value / 1000.0
        self.unified_speed_label.setText(f"{speed_sec:.1f}s")
        self.unified_animation_controller.set_animation_speed(value)
    
    def on_unified_step_changed(self, step_index, description):
        """统一动画步骤改变"""
        total_steps = len(self.unified_animation_controller.steps)
        if total_steps > 0:
            self.unified_progress_label.setText(f"{step_index}/{total_steps}")
        else:
            self.unified_progress_label.setText("0/0")
        self.unified_step_description.setText(description)
    
    def on_unified_animation_finished(self):
        """统一动画完成"""
        self.unified_progress_label.setText("完成")
        self.unified_step_description.setText("动画演示已结束")
        self.status_bar.showMessage("动画演示完成")
    
    def on_unified_status_changed(self, status):
        """统一动画状态改变"""
        self.status_bar.showMessage(status)

    def test_animation(self):
        """测试动画功能"""
        # 创建一个简单的二叉搜索树用于测试
        self.current_ds = "二叉搜索树"
        self.controls_panel.ds_combo.setCurrentText("二叉搜索树")

        # 清空并重新构建测试树
        self.bst.clear()
        test_values = [50, 30, 70, 20, 40, 60, 80]
        for value in test_values:
            self.bst.insert(value)

        # 更新显示
        self.update_display("创建测试二叉搜索树")

        # 手动触发一个简单的动画序列
        QTimer.singleShot(1000, self._animate_step1)
        QTimer.singleShot(2000, self._animate_step2)
        QTimer.singleShot(3000, self._animate_step3)

    def _animate_step1(self):
        """动画步骤1"""
        # 获取树的根节点ID
        if self.bst.root:
            root_id = self.bst.root.data['id']
            self.graphics_view.highlight_nodes([root_id], QColor(255, 0, 0), "高亮根节点")
            self.status_bar.showMessage("步骤1: 高亮根节点")

    def _animate_step2(self):
        """动画步骤2"""
        # 获取左子树节点ID
        if self.bst.root and self.bst.root.left:
            left_id = self.bst.root.left.data['id']
            self.graphics_view.highlight_nodes([left_id], QColor(0, 255, 0), "高亮左子节点")
            self.status_bar.showMessage("步骤2: 高亮左子节点")

    def _animate_step3(self):
        """动画步骤3"""
        # 获取右子树节点ID
        if self.bst.root and self.bst.root.right:
            right_id = self.bst.root.right.data['id']
            self.graphics_view.highlight_nodes([right_id], QColor(0, 0, 255), "高亮右子节点")
            self.status_bar.showMessage("步骤3: 高亮右子节点")