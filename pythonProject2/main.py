import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # 设置应用程序样式
    from utils.styles import apply_style
    apply_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()