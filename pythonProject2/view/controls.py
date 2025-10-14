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

        # 指令输入
        cmd_group = QGroupBox("指令输入")
        cmd_layout = QVBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("输入指令，如: insert 10 at beginning")
        self.execute_cmd_btn = QPushButton("执行指令")
        cmd_layout.addWidget(self.cmd_input)
        cmd_layout.addWidget(self.execute_cmd_btn)
        cmd_group.setLayout(cmd_layout)

        layout.addWidget(ds_group)
        layout.addWidget(self.ll_group)
        layout.addWidget(cmd_group)
        layout.addStretch()

        self.setLayout(layout)

    def connect_ll_signals(self, insert_begin, insert_end, insert_pos, delete_pos, clear):
        """连接链表操作的信号"""
        self.insert_begin_btn.clicked.connect(insert_begin)
        self.insert_end_btn.clicked.connect(insert_end)
        self.insert_pos_btn.clicked.connect(insert_pos)
        self.delete_pos_btn.clicked.connect(delete_pos)
        self.clear_btn.clicked.connect(clear)

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