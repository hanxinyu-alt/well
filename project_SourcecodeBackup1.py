# main.py - 主程序入口
import sys
from PyQt5.QtWidgets import QApplication
from app_window import MainWindow
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QLineEdit, QPushButton,
                             QGroupBox, QFormLayout, QTabWidget)
from calculator import CalculatorWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽油系统设计")
        self.setGeometry(100, 100, 1000, 800)
        self.init_ui()
        self.init_data()

    def init_ui(self):
        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左侧控制面板
        self.setup_control_panel(main_layout)

        # 右侧图表区域
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

    def setup_control_panel(self, main_layout):
        control_panel = QWidget()
        control_panel.setFixedWidth(400)
        control_layout = QVBoxLayout(control_panel)

        # 抽油机参数组
        self.setup_pump_parameters(control_layout)

        # 井参数组
        self.setup_well_parameters(control_layout)

        # 测试数据组
        self.setup_test_data(control_layout)

        # 设计参数组
        self.setup_design_parameters(control_layout)

        # 按钮区域
        self.setup_action_buttons(control_layout)

        main_layout.addWidget(control_panel)

    def setup_action_buttons(self, layout):
        button_group = QWidget()
        button_layout = QHBoxLayout(button_group)

        actions = [
            ("数据导入", self.import_data),
            ("井温曲线", self.show_temp_curve),
            ("粘温曲线", self.show_viscosity_curve),
            ("IPR曲线", self.show_ipr_curve),
            ("计算器", self.show_calculator)
        ]

        for text, callback in actions:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            button_layout.addWidget(btn)

        layout.addWidget(button_group)

    def show_calculator(self):
        self.calculator = CalculatorWindow()
        self.calculator.show()

    # 其他原有方法保持不变...
    # (包括init_data, on_model_changed, import_data等)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())