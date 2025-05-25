from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QLineEdit, QComboBox, QPushButton, QApplication)
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽油井系统设计")
        self.setup_ui()

    def setup_ui(self):
        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # 左侧基础数据区域
        left_group = QGroupBox("基础数据")
        left_layout = QVBoxLayout()

        # 油井参数输入
        self.add_parameter_input(left_layout, "油层深度(m)", "1765")
        self.add_parameter_input(left_layout, "套管直径(mm)", "190")
        self.add_parameter_input(left_layout, "油管内径(mm)", "88.9")
        self.add_parameter_input(left_layout, "井底温度(℃)", "87.6")
        self.add_parameter_input(left_layout, "地层压力(MPa)", "16.38")
        self.add_parameter_input(left_layout, "饱和压力(MPa)", "12.52")
        self.add_parameter_input(left_layout, "传热系数(W/m·℃)", "2.83")
        self.add_parameter_input(left_layout, "地温梯度(℃/100m)", "3.19")
        self.add_parameter_input(left_layout, "试井产液量(m³/d)", "27.7")
        self.add_parameter_input(left_layout, "试井流压(MPa)", "8.16")
        self.add_parameter_input(left_layout, "体积含水率(%)", "26.5")

        left_group.setLayout(left_layout)

        # 中间抽油机参数区域
        center_group = QGroupBox("抽油机参数")
        center_layout = QVBoxLayout()

        # 抽油机型号选择
        self.pump_type_combo = QComboBox()
        self.pump_type_combo.addItems(["CYJ5-1.8-18F", "CYJ7-2.1-26F", "CYJ10-3-53F"])
        center_layout.addWidget(QLabel("抽油机型号:"))
        center_layout.addWidget(self.pump_type_combo)

        # 冲程选择
        self.stroke_combo = QComboBox()
        center_layout.addWidget(QLabel("冲程(m):"))
        center_layout.addWidget(self.stroke_combo)

        # 冲次选择
        self.speed_combo = QComboBox()
        center_layout.addWidget(QLabel("冲次(min⁻¹):"))
        center_layout.addWidget(self.speed_combo)

        # 显示参数
        self.max_load_label = QLabel("最大载荷: 50 kN")
        self.max_torque_label = QLabel("最大扭矩: 13 kN·m")
        self.rod_length_label = QLabel("连杆长度: 2100 mm")
        self.crank_radius_label = QLabel("曲柄半径: 380 mm")

        center_layout.addWidget(self.max_load_label)
        center_layout.addWidget(self.max_torque_label)
        center_layout.addWidget(self.rod_length_label)
        center_layout.addWidget(self.crank_radius_label)

        center_group.setLayout(center_layout)

        # 右侧功能按钮区域
        right_group = QGroupBox("功能")
        right_layout = QVBoxLayout()

        # 曲线生成按钮
        self.add_function_button(right_layout, "井温曲线", self.show_temp_curve)
        self.add_function_button(right_layout, "粘温曲线", self.show_viscosity_curve)
        self.add_function_button(right_layout, "IPR曲线", self.show_ipr_curve)
        self.add_function_button(right_layout, "拟合粘温曲线", self.fit_viscosity_curve)

        # 计算按钮
        self.add_function_button(right_layout, "混合液密度计算", self.calculate_density)
        self.add_function_button(right_layout, "泵吸入口压力计算", self.calculate_suction_pressure)
        self.add_function_button(right_layout, "下泵深度计算", self.calculate_pump_depth)
        self.add_function_button(right_layout, "井底流压计算", self.calculate_bottom_pressure)
        self.add_function_button(right_layout, "计算泵径", self.calculate_pump_diameter)
        self.add_function_button(right_layout, "校核", self.verify_torque)
        self.add_function_button(right_layout, "计算电机功率", self.calculate_motor_power)

        right_group.setLayout(right_layout)

        # 添加到主布局
        main_layout.addWidget(left_group, 2)
        main_layout.addWidget(center_group, 1)
        main_layout.addWidget(right_group, 1)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # 连接信号
        self.pump_type_combo.currentIndexChanged.connect(self.update_pump_parameters)

    def add_parameter_input(self, layout, label, default=""):
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel(label))
        line_edit = QLineEdit(default)
        h_layout.addWidget(line_edit)
        layout.addLayout(h_layout)

    def add_function_button(self, layout, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

    def update_pump_parameters(self, index):
        # 根据选择的抽油机型号更新参数
        if index == 0:  # CYJ5-1.8-18F
            self.stroke_combo.clear()
            self.stroke_combo.addItems(["0.9", "1.2", "1.5", "1.8"])
            self.speed_combo.clear()
            self.speed_combo.addItems(["6", "9", "12"])
            self.max_load_label.setText("最大载荷: 50 kN")
            self.max_torque_label.setText("最大扭矩: 13 kN·m")
            self.rod_length_label.setText("连杆长度: 2100 mm")
        elif index == 1:  # CYJ7-2.1-26F
            self.stroke_combo.clear()
            self.stroke_combo.addItems(["1.1", "1.5", "1.9", "2.3", "2.7"])
            self.speed_combo.clear()
            self.speed_combo.addItems(["6", "9", "12"])
            self.max_load_label.setText("最大载荷: 50 kN")
            self.max_torque_label.setText("最大扭矩: 26 kN·m")
            self.rod_length_label.setText("连杆长度: 2137 mm")

    # 以下为各个功能的实现方法
    def show_temp_curve(self):
        from temp_curve import TempCurveWindow
        self.temp_curve = TempCurveWindow()
        self.temp_curve.show()

    def show_viscosity_curve(self, ViscosityCurveWindow=None):
        from self.viscosity_curve import ViscosityCurveWindow
        self.viscosity_curve = ViscosityCurveWindow()
        self.viscosity_curve.show()

    def show_ipr_curve(self):
        from ipr_curve import IPRCurveWindow
        self.ipr_curve = IPRCurveWindow()
        self.ipr_curve.show()

    def fit_viscosity_curve(self):
        # 实现拟合粘温曲线逻辑
        pass

    def calculate_density(self):
        # 实现混合液密度计算
        pass

    def calculate_suction_pressure(self):
        # 实现泵吸入口压力计算
        pass

    def calculate_pump_depth(self):
        # 实现下泵深度计算
        pass

    def calculate_bottom_pressure(self):
        # 实现井底流压计算
        pass

    def calculate_pump_diameter(self):
        # 实现泵径计算
        pass

    def verify_torque(self):
        # 实现扭矩校核
        pass

    def calculate_motor_power(self):
        # 实现电机功率计算
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())