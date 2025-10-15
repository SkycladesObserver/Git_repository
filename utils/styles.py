def apply_style(app):
    """应用样式表"""
    style = """
    QMainWindow {
        background-color: #f0f0f0;
    }

    QGroupBox {
        font-weight: bold;
        border: 2px solid #cccccc;
        border-radius: 5px;
        margin-top: 1ex;
        padding-top: 10px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
    }

    QPushButton {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 8px 16px;
        text-align: center;
        font-size: 14px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #45a049;
    }

    QPushButton:pressed {
        background-color: #3d8b40;
    }

    QSpinBox, QLineEdit, QComboBox {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
        background-color: white;
    }

    QLabel {
        font-size: 14px;
    }

    QStatusBar {
        background-color: #e0e0e0;
        color: #333333;
    }
    """

    app.setStyleSheet(style)