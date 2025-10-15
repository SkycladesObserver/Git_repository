from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QSpinBox, QLabel, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt


class ControlsPanel(QWidget):
    """控制面板"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 数据结构选择
        ds_group = QGroupBox("数据结构选择")
        ds_layout = QHBoxLayout()
        self.ds_combo = QComboBox()
        self.ds_combo.addItems(["链表", "栈", "队列", "二叉树", "二叉搜索树"])
        ds_layout.addWidget(QLabel("选择数据结构:"))
        ds_layout.addWidget(self.ds_combo)
        ds_layout.addStretch()
        ds_group.setLayout(ds_layout)

        # 链表操作组
        self.ll_group = QGroupBox("链表操作")
        ll_layout = QVBoxLayout()

        # 值输入
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("值:"))
        self.value_spin = QSpinBox()
        self.value_spin.setRange(-999, 999)
        self.value_spin.setValue(10)
        value_layout.addWidget(self.value_spin)
        value_layout.addStretch()

        # 位置输入
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("位置:"))
        self.position_spin = QSpinBox()
        self.position_spin.setRange(0, 99)
        self.position_spin.setValue(0)
        position_layout.addWidget(self.position_spin)
        position_layout.addStretch()

        # 操作按钮
        button_layout = QHBoxLayout()
        self.insert_begin_btn = QPushButton("在开头插入")
        self.insert_end_btn = QPushButton("在末尾插入")
        self.insert_pos_btn = QPushButton("在指定位置插入")
        self.delete_pos_btn = QPushButton("删除指定位置")
        self.clear_btn = QPushButton("清空链表")

        button_layout.addWidget(self.insert_begin_btn)
        button_layout.addWidget(self.insert_end_btn)
        button_layout.addWidget(self.insert_pos_btn)
        button_layout.addWidget(self.delete_pos_btn)
        button_layout.addWidget(self.clear_btn)

        ll_layout.addLayout(value_layout)
        ll_layout.addLayout(position_layout)
        ll_layout.addLayout(button_layout)
        self.ll_group.setLayout(ll_layout)

        # 栈操作组
        self.stack_group = QGroupBox("栈操作")
        stack_layout = QVBoxLayout()

        # 栈值输入
        stack_value_layout = QHBoxLayout()
        stack_value_layout.addWidget(QLabel("值:"))
        self.stack_value_spin = QSpinBox()
        self.stack_value_spin.setRange(-999, 999)
        self.stack_value_spin.setValue(10)
        stack_value_layout.addWidget(self.stack_value_spin)
        stack_value_layout.addStretch()

        # 栈操作按钮
        stack_button_layout = QHBoxLayout()
        self.push_btn = QPushButton("入栈")
        self.pop_btn = QPushButton("出栈")
        self.clear_stack_btn = QPushButton("清空栈")

        stack_button_layout.addWidget(self.push_btn)
        stack_button_layout.addWidget(self.pop_btn)
        stack_button_layout.addWidget(self.clear_stack_btn)

        stack_layout.addLayout(stack_value_layout)
        stack_layout.addLayout(stack_button_layout)
        self.stack_group.setLayout(stack_layout)
        self.stack_group.setVisible(False)  # 默认隐藏

        # 队列操作组
        self.queue_group = QGroupBox("队列操作")
        queue_layout = QVBoxLayout()

        # 队列值输入
        queue_value_layout = QHBoxLayout()
        queue_value_layout.addWidget(QLabel("值:"))
        self.queue_value_spin = QSpinBox()
        self.queue_value_spin.setRange(-999, 999)
        self.queue_value_spin.setValue(10)
        queue_value_layout.addWidget(self.queue_value_spin)
        queue_value_layout.addStretch()

        # 队列操作按钮
        queue_button_layout = QHBoxLayout()
        self.enqueue_btn = QPushButton("入队")
        self.dequeue_btn = QPushButton("出队")
        self.clear_queue_btn = QPushButton("清空队列")

        queue_button_layout.addWidget(self.enqueue_btn)
        queue_button_layout.addWidget(self.dequeue_btn)
        queue_button_layout.addWidget(self.clear_queue_btn)

        queue_layout.addLayout(queue_value_layout)
        queue_layout.addLayout(queue_button_layout)
        self.queue_group.setLayout(queue_layout)
        self.queue_group.setVisible(False)  # 默认隐藏

        # 指令输入
        cmd_group = QGroupBox("指令输入")
        cmd_layout = QVBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("输入指令，如: insert 10 at beginning 或 push 5 或 enqueue 8")
        self.execute_cmd_btn = QPushButton("执行指令")
        cmd_layout.addWidget(self.cmd_input)
        cmd_layout.addWidget(self.execute_cmd_btn)
        cmd_group.setLayout(cmd_layout)

        layout.addWidget(ds_group)
        layout.addWidget(self.ll_group)
        layout.addWidget(self.stack_group)
        layout.addWidget(self.queue_group)
        layout.addWidget(cmd_group)
        layout.addStretch()

        self.setLayout(layout)

        # 连接数据结构选择信号
        self.ds_combo.currentTextChanged.connect(self.on_ds_changed)

    def on_ds_changed(self, ds_name):
        """当数据结构改变时显示对应的操作组"""
        self.ll_group.setVisible(ds_name == "链表")
        self.stack_group.setVisible(ds_name == "栈")
        self.queue_group.setVisible(ds_name == "队列")


    def connect_ll_signals(self, insert_begin, insert_end, insert_pos, delete_pos, clear):
        """连接链表操作的信号"""
        self.insert_begin_btn.clicked.connect(insert_begin)
        self.insert_end_btn.clicked.connect(insert_end)
        self.insert_pos_btn.clicked.connect(insert_pos)
        self.delete_pos_btn.clicked.connect(delete_pos)
        self.clear_btn.clicked.connect(clear)

    def connect_stack_signals(self, push, pop, clear):
        """连接栈操作的信号"""
        self.push_btn.clicked.connect(push)
        self.pop_btn.clicked.connect(pop)
        self.clear_stack_btn.clicked.connect(clear)

    def connect_queue_signals(self, enqueue, dequeue, clear):
        """连接队列操作的信号"""
        self.enqueue_btn.clicked.connect(enqueue)
        self.dequeue_btn.clicked.connect(dequeue)
        self.clear_queue_btn.clicked.connect(clear)

    def get_value(self):
        """获取输入的值"""
        return self.value_spin.value()

    def get_position(self):
        """获取输入的位置"""
        return self.position_spin.value()

    def get_command(self):
        """获取指令"""
        return self.cmd_input.text().strip()

    def clear_command(self):
        """清空指令输入"""
        self.cmd_input.clear()

