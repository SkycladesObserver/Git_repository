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

        # 快速操作栏
        quick_action_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存")
        self.load_btn = QPushButton("加载")
        self.help_btn = QPushButton("帮助")

        quick_action_layout.addWidget(self.save_btn)
        quick_action_layout.addWidget(self.load_btn)
        quick_action_layout.addWidget(self.help_btn)
        quick_action_layout.addStretch()

        # 数据结构选择
        ds_group = QGroupBox("数据结构选择")
        ds_layout = QHBoxLayout()
        self.ds_combo = QComboBox()
        self.ds_combo.addItems(["链表", "栈", "队列", "二叉树", "二叉搜索树", "哈夫曼树", "AVL树"])
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
        self.stack_group.setVisible(False)

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
        self.queue_group.setVisible(False)

        # 二叉树操作组
        self.binary_tree_group = QGroupBox("二叉树操作")
        binary_tree_layout = QVBoxLayout()

        # 二叉树值输入
        bt_value_layout = QHBoxLayout()
        bt_value_layout.addWidget(QLabel("值:"))
        self.bt_value_spin = QSpinBox()
        self.bt_value_spin.setRange(-999, 999)
        self.bt_value_spin.setValue(10)
        bt_value_layout.addWidget(self.bt_value_spin)
        bt_value_layout.addStretch()

        # 二叉树操作按钮
        bt_button_layout = QHBoxLayout()
        self.bt_insert_level_btn = QPushButton("层次插入")
        self.bt_clear_btn = QPushButton("清空二叉树")

        bt_button_layout.addWidget(self.bt_insert_level_btn)
        bt_button_layout.addWidget(self.bt_clear_btn)

        # 批量插入
        bt_batch_layout = QHBoxLayout()
        self.bt_batch_input = QLineEdit()
        self.bt_batch_input.setPlaceholderText("输入多个值，用逗号分隔，如: 1,2,3,4,5")
        self.bt_batch_insert_btn = QPushButton("批量插入")

        bt_batch_layout.addWidget(self.bt_batch_input)
        bt_batch_layout.addWidget(self.bt_batch_insert_btn)

        binary_tree_layout.addLayout(bt_value_layout)
        binary_tree_layout.addLayout(bt_button_layout)
        binary_tree_layout.addLayout(bt_batch_layout)
        self.binary_tree_group.setLayout(binary_tree_layout)
        self.binary_tree_group.setVisible(False)

        # 二叉搜索树操作组
        self.bst_group = QGroupBox("二叉搜索树操作")
        bst_layout = QVBoxLayout()

        # BST值输入
        bst_value_layout = QHBoxLayout()
        bst_value_layout.addWidget(QLabel("值:"))
        self.bst_value_spin = QSpinBox()
        self.bst_value_spin.setRange(-999, 999)
        self.bst_value_spin.setValue(10)
        bst_value_layout.addWidget(self.bst_value_spin)
        bst_value_layout.addStretch()

        # BST操作按钮
        bst_button_layout = QHBoxLayout()
        self.bst_insert_btn = QPushButton("插入")
        self.bst_search_btn = QPushButton("查找")
        self.bst_delete_btn = QPushButton("删除")
        self.bst_clear_btn = QPushButton("清空BST")

        bst_button_layout.addWidget(self.bst_insert_btn)
        bst_button_layout.addWidget(self.bst_search_btn)
        bst_button_layout.addWidget(self.bst_delete_btn)
        bst_button_layout.addWidget(self.bst_clear_btn)

        # BST批量插入
        bst_batch_layout = QHBoxLayout()
        self.bst_batch_input = QLineEdit()
        self.bst_batch_input.setPlaceholderText("输入多个值，用逗号分隔，如: 5,3,7,2,4,6,8")
        self.bst_batch_insert_btn = QPushButton("批量插入")

        bst_batch_layout.addWidget(self.bst_batch_input)
        bst_batch_layout.addWidget(self.bst_batch_insert_btn)

        bst_layout.addLayout(bst_value_layout)
        bst_layout.addLayout(bst_button_layout)
        bst_layout.addLayout(bst_batch_layout)
        self.bst_group.setLayout(bst_layout)
        self.bst_group.setVisible(False)

        # 哈夫曼树操作组
        self.huffman_group = QGroupBox("哈夫曼树操作")
        huffman_layout = QVBoxLayout()

        # 文本输入
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("文本:"))
        self.huffman_text_input = QLineEdit()
        self.huffman_text_input.setPlaceholderText("输入要编码的文本")
        text_layout.addWidget(self.huffman_text_input)

        # 频率输入
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("频率(字符:频率):"))
        self.huffman_freq_input = QLineEdit()
        self.huffman_freq_input.setPlaceholderText("如: a:5,b:3,c:2")
        freq_layout.addWidget(self.huffman_freq_input)

        # 操作按钮
        huffman_button_layout = QHBoxLayout()
        self.huffman_build_text_btn = QPushButton("从文本构建")
        self.huffman_build_freq_btn = QPushButton("从频率构建")
        self.huffman_encode_btn = QPushButton("编码")
        self.huffman_decode_btn = QPushButton("解码")
        self.huffman_clear_btn = QPushButton("清空")

        huffman_button_layout.addWidget(self.huffman_build_text_btn)
        huffman_button_layout.addWidget(self.huffman_build_freq_btn)
        huffman_button_layout.addWidget(self.huffman_encode_btn)
        huffman_button_layout.addWidget(self.huffman_decode_btn)
        huffman_button_layout.addWidget(self.huffman_clear_btn)

        huffman_layout.addLayout(text_layout)
        huffman_layout.addLayout(freq_layout)
        huffman_layout.addLayout(huffman_button_layout)
        self.huffman_group.setLayout(huffman_layout)
        self.huffman_group.setVisible(False)

        # AVL树操作组
        self.avl_group = QGroupBox("AVL树操作")
        avl_layout = QVBoxLayout()

        # AVL值输入
        avl_value_layout = QHBoxLayout()
        avl_value_layout.addWidget(QLabel("值:"))
        self.avl_value_spin = QSpinBox()
        self.avl_value_spin.setRange(-999, 999)
        self.avl_value_spin.setValue(10)
        avl_value_layout.addWidget(self.avl_value_spin)
        avl_value_layout.addStretch()

        # AVL操作按钮
        avl_button_layout = QHBoxLayout()
        self.avl_insert_btn = QPushButton("插入")
        self.avl_search_btn = QPushButton("查找")
        self.avl_delete_btn = QPushButton("删除")
        self.avl_clear_btn = QPushButton("清空AVL")

        avl_button_layout.addWidget(self.avl_insert_btn)
        avl_button_layout.addWidget(self.avl_search_btn)
        avl_button_layout.addWidget(self.avl_delete_btn)
        avl_button_layout.addWidget(self.avl_clear_btn)

        # AVL批量插入
        avl_batch_layout = QHBoxLayout()
        self.avl_batch_input = QLineEdit()
        self.avl_batch_input.setPlaceholderText("输入多个值，用逗号分隔，如: 10,20,5,15,25")
        self.avl_batch_insert_btn = QPushButton("批量插入")

        avl_batch_layout.addWidget(self.avl_batch_input)
        avl_batch_layout.addWidget(self.avl_batch_insert_btn)

        avl_layout.addLayout(avl_value_layout)
        avl_layout.addLayout(avl_button_layout)
        avl_layout.addLayout(avl_batch_layout)
        self.avl_group.setLayout(avl_layout)
        self.avl_group.setVisible(False)

        # 指令输入
        cmd_group = QGroupBox("指令输入")
        cmd_layout = QVBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("输入指令，如: insert 10 at beginning 或 avl_insert 15")
        self.execute_cmd_btn = QPushButton("执行指令")
        cmd_layout.addWidget(self.cmd_input)
        cmd_layout.addWidget(self.execute_cmd_btn)
        cmd_group.setLayout(cmd_layout)

        layout.addLayout(quick_action_layout)
        layout.addWidget(ds_group)
        layout.addWidget(self.ll_group)
        layout.addWidget(self.stack_group)
        layout.addWidget(self.queue_group)
        layout.addWidget(self.binary_tree_group)
        layout.addWidget(self.bst_group)
        layout.addWidget(self.huffman_group)
        layout.addWidget(self.avl_group)
        layout.addWidget(cmd_group)
        layout.addStretch()

        self.setLayout(layout)

        # 连接数据结构选择信号
        self.ds_combo.currentTextChanged.connect(self.on_ds_changed)

    def connect_file_signals(self, save, load, help):
        """连接文件操作的信号"""
        self.save_btn.clicked.connect(save)
        self.load_btn.clicked.connect(load)
        self.help_btn.clicked.connect(help)

    def on_ds_changed(self, ds_name):
        """当数据结构改变时显示对应的操作组"""
        self.ll_group.setVisible(ds_name == "链表")
        self.stack_group.setVisible(ds_name == "栈")
        self.queue_group.setVisible(ds_name == "队列")
        self.binary_tree_group.setVisible(ds_name == "二叉树")
        self.bst_group.setVisible(ds_name == "二叉搜索树")
        self.huffman_group.setVisible(ds_name == "哈夫曼树")
        self.avl_group.setVisible(ds_name == "AVL树")

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

    def connect_binary_tree_signals(self, insert_level, clear, batch_insert):
        """连接二叉树操作的信号"""
        self.bt_insert_level_btn.clicked.connect(insert_level)
        self.bt_clear_btn.clicked.connect(clear)
        self.bt_batch_insert_btn.clicked.connect(batch_insert)

    def connect_avl_signals(self, insert, search, delete, clear, batch_insert):
        """连接AVL树操作的信号"""
        self.avl_insert_btn.clicked.connect(insert)
        self.avl_search_btn.clicked.connect(search)
        self.avl_delete_btn.clicked.connect(delete)
        self.avl_clear_btn.clicked.connect(clear)
        self.avl_batch_insert_btn.clicked.connect(batch_insert)

    def get_avl_batch_values(self):
        """获取AVL批量插入的值"""
        text = self.avl_batch_input.text().strip()
        if not text:
            return []

        try:
            values = [int(x.strip()) for x in text.split(',')]
            return values
        except ValueError:
            return []

    def clear_avl_batch_input(self):
        """清空AVL批量输入框"""
        self.avl_batch_input.clear()

    def get_binary_tree_batch_values(self):
        """获取批量插入的值"""
        text = self.bt_batch_input.text().strip()
        if not text:
            return []

        try:
            values = [int(x.strip()) for x in text.split(',')]
            return values
        except ValueError:
            return []

    def clear_binary_tree_batch_input(self):
        """清空批量输入框"""
        self.bt_batch_input.clear()

    def connect_bst_signals(self, insert, search, delete, clear, batch_insert):
        """连接二叉搜索树操作的信号"""
        self.bst_insert_btn.clicked.connect(insert)
        self.bst_search_btn.clicked.connect(search)
        self.bst_delete_btn.clicked.connect(delete)
        self.bst_clear_btn.clicked.connect(clear)
        self.bst_batch_insert_btn.clicked.connect(batch_insert)

    def get_bst_batch_values(self):
        """获取BST批量插入的值"""
        text = self.bst_batch_input.text().strip()
        if not text:
            return []

        try:
            values = [int(x.strip()) for x in text.split(',')]
            return values
        except ValueError:
            return []

    def clear_bst_batch_input(self):
        """清空BST批量输入框"""
        self.bst_batch_input.clear()

    def connect_huffman_signals(self, build_from_text, build_from_freq, encode, decode, clear):
        """连接哈夫曼树操作的信号"""
        self.huffman_build_text_btn.clicked.connect(build_from_text)
        self.huffman_build_freq_btn.clicked.connect(build_from_freq)
        self.huffman_encode_btn.clicked.connect(encode)
        self.huffman_decode_btn.clicked.connect(decode)
        self.huffman_clear_btn.clicked.connect(clear)

    def get_huffman_text(self):
        """获取哈夫曼文本输入"""
        return self.huffman_text_input.text().strip()

    def get_huffman_frequency(self):
        """获取哈夫曼频率输入"""
        text = self.huffman_freq_input.text().strip()
        if not text:
            return {}

        try:
            frequency = {}
            pairs = text.split(',')
            for pair in pairs:
                char, freq = pair.split(':')
                frequency[char.strip()] = int(freq.strip())
            return frequency
        except ValueError:
            return {}

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

