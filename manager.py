from PyQt5.QtCore import QObject


class CalculatorManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.core = CalculatorCore()
        self.ui = CalculatorUI(self.core)

    def show(self):
        self.ui.show()