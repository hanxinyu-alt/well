import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QGridLayout, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5计算器")
        self.setFixedSize(300, 400)

        # 主部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 显示框
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; border: 1px solid #ccc;")
        main_layout.addWidget(self.display)

        # 按钮布局
        grid = QGridLayout()
        main_layout.addLayout(grid)

        # 按钮定义
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        # 创建按钮
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 18px; min-height: 50px;")
            button.clicked.connect(self.on_button_click)
            grid.addWidget(button, row, col)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        current_text = self.display.text()

        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                result = str(eval(current_text))
                self.display.setText(result)
            except:
                self.display.setText("Error")
        else:
            self.display.setText(current_text + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())