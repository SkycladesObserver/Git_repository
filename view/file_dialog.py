from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
import os
import json


class FileDialog(QDialog):
    """文件操作对话框"""

    def __init__(self, parent=None, mode="save"):
        super().__init__(parent)
        self.mode = mode  # "save" 或 "load"
        self.selected_file = None
        self.init_ui()

        if mode == "load":
            self.load_file_list()

    def init_ui(self):
        """初始化UI"""
        if self.mode == "save":
            self.setWindowTitle("保存数据结构")
        else:
            self.setWindowTitle("加载数据结构")

        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("选择文件:")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title_label)

        # 文件列表
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.on_file_selected)
        layout.addWidget(self.file_list)

        # 按钮布局
        button_layout = QHBoxLayout()

        if self.mode == "save":
            self.save_btn = QPushButton("保存为新文件")
            self.save_btn.clicked.connect(self.save_as_new)
            button_layout.addWidget(self.save_btn)

            self.overwrite_btn = QPushButton("覆盖选中文件")
            self.overwrite_btn.clicked.connect(self.overwrite_file)
            self.overwrite_btn.setEnabled(False)
            button_layout.addWidget(self.overwrite_btn)
        else:
            self.load_btn = QPushButton("加载选中文件")
            self.load_btn.clicked.connect(self.load_file)
            self.load_btn.setEnabled(False)
            button_layout.addWidget(self.load_btn)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 连接选择事件
        self.file_list.itemSelectionChanged.connect(self.on_selection_changed)

    def load_file_list(self):
        """加载文件列表"""
        self.file_list.clear()

        # 查找保存目录
        save_dir = self.get_save_directory()
        if not os.path.exists(save_dir):
            return

        # 添加所有 .dsv 文件（Data Structure Visualization）
        for filename in os.listdir(save_dir):
            if filename.endswith('.dsv'):
                self.file_list.addItem(filename)

    def get_save_directory(self):
        """获取保存目录"""
        # 在当前目录下创建 saves 文件夹
        save_dir = os.path.join(os.getcwd(), "saves")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return save_dir

    def on_selection_changed(self):
        """当选择改变时"""
        if self.mode == "save":
            self.overwrite_btn.setEnabled(len(self.file_list.selectedItems()) > 0)
        else:
            self.load_btn.setEnabled(len(self.file_list.selectedItems()) > 0)

    def on_file_selected(self, item):
        """当双击文件时"""
        if self.mode == "save":
            self.overwrite_file()
        else:
            self.load_file()

    def save_as_new(self):
        """保存为新文件"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存数据结构",
            self.get_save_directory(),
            "Data Structure Files (*.dsv)"
        )

        if filename:
            if not filename.endswith('.dsv'):
                filename += '.dsv'
            self.selected_file = filename
            self.accept()

    def overwrite_file(self):
        """覆盖选中文件"""
        selected_items = self.file_list.selectedItems()
        if selected_items:
            filename = selected_items[0].text()
            self.selected_file = os.path.join(self.get_save_directory(), filename)
            self.accept()

    def load_file(self):
        """加载选中文件"""
        selected_items = self.file_list.selectedItems()
        if selected_items:
            filename = selected_items[0].text()
            self.selected_file = os.path.join(self.get_save_directory(), filename)
            self.accept()

    def get_selected_file(self):
        """获取选中的文件"""
        return self.selected_file