from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar
from PyQt5.QtCore import Qt
from .graphics_view import GraphicsView
from .controls import ControlsPanel
from model.linked_list import LinkedList


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.linked_list = LinkedList()
        self.init_ui()
        self.connect_signals()

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
        # 连接链表操作
        self.controls_panel.connect_ll_signals(
            self.insert_beginning,
            self.insert_end,
            self.insert_at_position,
            self.delete_at_position,
            self.clear_list
        )

        # 连接指令执行
        self.controls_panel.execute_cmd_btn.clicked.connect(self.execute_command)

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

    def execute_command(self):
        """执行指令"""
        command = self.controls_panel.get_command()
        if not command:
            return

        # 简化版指令解析
        parts = command.lower().split()
        if len(parts) >= 2 and parts[0] == "insert":
            try:
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
            except (ValueError, IndexError) as e:
                self.status_bar.showMessage(f"指令错误: {str(e)}")

        elif len(parts) >= 2 and parts[0] == "delete":
            if "position" in command and len(parts) > 2:
                try:
                    position = int(parts[2])
                    deleted_node = self.linked_list.delete_at_position(position)
                    self.update_display(f"指令执行: {command}")
                except (ValueError, IndexError) as e:
                    self.status_bar.showMessage(f"指令错误: {str(e)}")

        elif command == "clear":
            self.linked_list.clear()
            self.update_display("指令执行: 清空链表")

        else:
            self.status_bar.showMessage(f"未知指令: {command}")

        self.controls_panel.clear_command()

    def update_display(self, message=None):
        """更新显示"""
        if message:
            self.status_bar.showMessage(message)
            self.graphics_view.add_operation_text(message)

        # 确保链表不为空时才绘制
        if hasattr(self, 'linked_list') and self.linked_list.head is not None:
            self.graphics_view.draw_linked_list(self.linked_list)
        else:
            # 如果链表为空，清空显示
            self.graphics_view.clear_scene()
            if message:
                self.graphics_view.add_operation_text(message)