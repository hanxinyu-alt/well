import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class RodDesignWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽油杆柱设计")
        self.setGeometry(100, 100, 400, 500)

        # 初始化数据
        self.allowable_stresses = ["50", "60", "70", "80", "90", "100"]
        self.rod_diameters = [16, 19, 22, 25, 29]  # 抽油杆直径(mm)
        self.steel_density = 7850  # 钢材密度(kg/m³)
        self.gravity = 9.81  # 重力加速度(m/s²)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # 标题
        title_label = QLabel("抽油杆柱设计")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # 许用应力选择
        stress_layout = QHBoxLayout()
        stress_label = QLabel("许用应力(N/mm²):")
        self.stress_combo = QComboBox()
        self.stress_combo.addItems(self.allowable_stresses)
        self.stress_combo.setCurrentIndex(-1)
        self.stress_combo.setPlaceholderText("请选择")
        stress_layout.addWidget(stress_label)
        stress_layout.addWidget(self.stress_combo)
        layout.addLayout(stress_layout)

        # 杆长度输入
        self.length_inputs = []
        for i in range(5):
            level = ["一级", "二级", "三级", "四级", "五级"][i]
            input_layout = QHBoxLayout()
            label = QLabel(f"{level}杆长度(m):")
            input_field = QLineEdit()
            input_field.setPlaceholderText("0.00")
            self.length_inputs.append(input_field)
            input_layout.addWidget(label)
            input_layout.addWidget(input_field)
            layout.addLayout(input_layout)

        # 载荷输入
        max_load_layout = QHBoxLayout()
        max_load_label = QLabel("最大载荷(N):")
        self.max_load_input = QLineEdit()
        self.max_load_input.setPlaceholderText("输入最大载荷")
        max_load_layout.addWidget(max_load_label)
        max_load_layout.addWidget(self.max_load_input)
        layout.addLayout(max_load_layout)

        min_load_layout = QHBoxLayout()
        min_load_label = QLabel("最小载荷(N):")
        self.min_load_input = QLineEdit()
        self.min_load_input.setPlaceholderText("输入最小载荷")
        min_load_layout.addWidget(min_load_label)
        min_load_layout.addWidget(self.min_load_input)
        layout.addLayout(min_load_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.check_btn = QPushButton("校核")
        self.check_btn.clicked.connect(self.check_design)
        self.calc_btn = QPushButton("计算")
        self.calc_btn.clicked.connect(self.calculate)
        button_layout.addWidget(self.check_btn)
        button_layout.addWidget(self.calc_btn)
        layout.addLayout(button_layout)

        # 结果展示
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignLeft)
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                min-width: 100px;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #aaa;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

    def check_design(self):
        """校核设计"""
        try:
            # 获取输入值
            stress = float(self.stress_combo.currentText())
            max_load = float(self.max_load_input.text())
            min_load = float(self.min_load_input.text())

            # 计算应力幅和平均应力
            stress_amplitude = (max_load - min_load) / 2
            mean_stress = (max_load + min_load) / 2

            # 计算应力比
            stress_ratio = stress_amplitude / stress

            # 校核结果
            if stress_ratio < 0.8:
                result = "设计安全，应力比为{:.2f}".format(stress_ratio)
            else:
                result = "警告：应力比过高({:.2f})，请重新设计".format(stress_ratio)

            self.result_label.setText(result)

        except Exception as e:
            QMessageBox.warning(self, "输入错误", "请输入有效的数值")

    def calculate(self):
        """执行计算"""
        try:
            # 获取输入值
            stress = float(self.stress_combo.currentText())
            rod_lengths = [float(input.text()) if input.text() else 0 for input in self.length_inputs]
            max_load = float(self.max_load_input.text())
            min_load = float(self.min_load_input.text())

            # 计算总长度和总重量
            total_length = sum(rod_lengths)

            # 计算杆柱总重量
            total_weight = 0
            for i, length in enumerate(rod_lengths):
                if length > 0:
                    diameter = self.rod_diameters[i] / 1000  # 转换为m
                    cross_area = math.pi * (diameter **  2) / 4  # 截面积(m²)
                    weight = cross_area * length * self.steel_density * self.gravity  # 单根杆重量(N)
                    total_weight += weight

            # 计算应力参数
            stress_amplitude = (max_load - min_load) / 2
            mean_stress = (max_load + min_load) / 2
            stress_ratio = stress_amplitude / stress

            # 计算结果
            result = (
                f"计算结果:\n"
                f"总杆柱长度: {total_length:.2f}m\n"
                f"杆柱总重量: {total_weight:.2f}N\n"
                f"最大应力: {max_load:.2f}N\n"
                f"最小应力: {min_load:.2f}N\n"
                f"应力幅: {stress_amplitude:.2f}N/mm²\n"
                f"应力比: {stress_ratio:.2f}"
            )

            self.result_label.setText(result)

        except Exception as e:
            QMessageBox.warning(self, "输入错误", "请输入有效的数值")


class PumpSystemDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽油机系统设计工具")
        self.setGeometry(100, 100, 600, 500)

        # 初始化数据
        self.pump_types = [
            "CYJ5-1.8-18F", "CYJ7-2.1-26F", "CYJ10-3-53B",
            "CYJ12-4.8-73HB", "CYJ14-5-73HQ"
        ]

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("抽油机系统设计工具")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # 抽油杆设计按钮
        rod_design_btn = QPushButton("抽油杆柱设计")
        rod_design_btn.clicked.connect(self.show_rod_design)
        layout.addWidget(rod_design_btn)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def show_rod_design(self):
        """显示抽油杆设计窗口"""
        self.rod_design_window = RodDesignWindow()
        self.rod_design_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PumpSystemDesigner()
    window.show()
    sys.exit(app.exec_())