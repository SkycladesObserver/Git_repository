from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar
from PyQt5.QtCore import Qt
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
        self.linked_list.insert_at_beginning(value)
        self.update_display(f"在开头插入节点: {value}")

    def insert_end(self):
        """在链表末尾插入节点"""
        value = self.controls_panel.get_value()
        self.linked_list.insert_at_end(value)
        self.update_display(f"在末尾插入节点: {value}")

    def insert_at_position(self):
        """在指定位置插入节点"""
        value = self.controls_panel.get_value()
        position = self.controls_panel.get_position()

        try:
            self.linked_list.insert_at_position(position, value)
            self.update_display(f"在位置 {position} 插入节点: {value}")
        except IndexError as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def delete_at_position(self):
        """删除指定位置的节点"""
        position = self.controls_panel.get_position()

        try:
            deleted_node = self.linked_list.delete_at_position(position)
            self.update_display(f"删除位置 {position} 的节点: {deleted_node.data}")
        except IndexError as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_list(self):
        """清空链表"""
        self.linked_list.clear()
        self.update_display("链表已清空")

    # 栈操作方法
    def push(self):
        """入栈操作"""
        value = self.controls_panel.stack_value_spin.value()
        try:
            self.stack.push(value)
            self.update_display(f"入栈: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def pop(self):
        """出栈操作"""
        try:
            value = self.stack.pop()
            self.update_display(f"出栈: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_stack(self):
        """清空栈"""
        self.stack = Stack()
        self.update_display("栈已清空")

    # 队列操作方法
    def enqueue(self):
        """入队操作"""
        value = self.controls_panel.queue_value_spin.value()
        try:
            self.queue.enqueue(value)
            self.update_display(f"入队: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def dequeue(self):
        """出队操作"""
        try:
            value = self.queue.dequeue()
            self.update_display(f"出队: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def clear_queue(self):
        """清空队列"""
        self.queue = Queue()
        self.update_display("队列已清空")

    # 二叉树操作方法

    def binary_tree_insert_level(self):
        """二叉树层次插入"""
        value = self.controls_panel.bt_value_spin.value()

        try:
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
        self.binary_tree = BinaryTree()
        self.update_display("二叉树已清空")

    # 二叉搜索树操作方法
    def bst_insert(self):
        """BST插入"""
        value = self.controls_panel.bst_value_spin.value()
        try:
            self.bst.insert(value)
            self.update_display(f"BST插入: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def bst_search(self):
        """BST查找"""
        value = self.controls_panel.bst_value_spin.value()
        node = self.bst.search(value)
        if node:
            self.update_display(f"BST查找: 找到 {value}")
        else:
            self.update_display(f"BST查找: 未找到 {value}")

    def bst_delete(self):
        """BST删除"""
        value = self.controls_panel.bst_value_spin.value()
        try:
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
            self.avl_tree.insert(value)
            self.update_display(f"AVL插入: {value}")
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}")

    def avl_search(self):
        """AVL查找"""
        value = self.controls_panel.avl_value_spin.value()
        node = self.avl_tree.search(value)
        if node:
            self.update_display(f"AVL查找: 找到 {value}")
        else:
            self.update_display(f"AVL查找: 未找到 {value}")

    def avl_delete(self):
        """AVL删除"""
        value = self.controls_panel.avl_value_spin.value()
        try:
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