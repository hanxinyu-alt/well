from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton


class CalculatorUI(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.init_ui()

    def init_ui(self):
        # 界面布局实现
        self.display = QLineEdit()
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'C', '+',
            '='
        ]
        # ... 布局实现代码