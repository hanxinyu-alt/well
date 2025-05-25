import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 测试窗体")
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

        # 添加一个按钮
        self.button = QPushButton("点击我", self)
        self.button.move(100, 80)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        print("按钮被点击了！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
