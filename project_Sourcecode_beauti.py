import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QLineEdit, QPushButton, QGroupBox, QFormLayout,
                             QTabWidget, QScrollArea)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton
from manager import CalculatorManager


class MainWindow(QMainWindow):
    def __init__(self):
        # ... 原有代码
        self.calculator = CalculatorManager()

        # 添加计算器按钮
        btn_calc = QPushButton("打开计算器")
        btn_calc.clicked.connect(self.calculator.show)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("韩鑫宇抽油系统设计")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左侧控制面板
        control_panel = QWidget()
        control_panel.setFixedWidth(400)
        control_layout = QVBoxLayout(control_panel)

        # 抽油机型号选择
        group_model = QGroupBox("抽油机参数韩鑫宇")
        form_model = QFormLayout()

        self.combo_model = QComboBox()
        self.combo_model.addItems([f"型号{i}" for i in range(16)])
        self.combo_model.currentIndexChanged.connect(self.on_model_changed)
        form_model.addRow("抽油机型号:", self.combo_model)

        self.combo_stroke = QComboBox()
        form_model.addRow("冲程(m):", self.combo_stroke)

        self.combo_stroke_times = QComboBox()
        form_model.addRow("冲次(次/min):", self.combo_stroke_times)

        self.edit_max_load = QLineEdit()
        self.edit_max_load.setReadOnly(True)
        form_model.addRow("最大载荷(kN):", self.edit_max_load)

        self.edit_max_torque = QLineEdit()
        self.edit_max_torque.setReadOnly(True)
        form_model.addRow("最大扭矩(kN·m):", self.edit_max_torque)

        self.edit_rod_length = QLineEdit()
        self.edit_rod_length.setReadOnly(True)
        form_model.addRow("连杆长度(mm):", self.edit_rod_length)

        self.edit_crank_radius = QLineEdit()
        form_model.addRow("曲柄半径(mm):", self.edit_crank_radius)

        group_model.setLayout(form_model)
        control_layout.addWidget(group_model)

        # 井参数
        group_well = QGroupBox("井参数")
        form_well = QFormLayout()

        self.edit_oil_depth = QLineEdit()
        form_well.addRow("油层深度(m):", self.edit_oil_depth)

        self.edit_casing_diameter = QLineEdit()
        form_well.addRow("套管内径(mm):", self.edit_casing_diameter)

        self.edit_tubing_diameter = QLineEdit()
        form_well.addRow("油管内径(mm):", self.edit_tubing_diameter)

        self.edit_bottom_temp = QLineEdit()
        form_well.addRow("井底温度(℃):", self.edit_bottom_temp)

        self.edit_formation_pressure = QLineEdit()
        form_well.addRow("地层压力(MPa):", self.edit_formation_pressure)

        self.edit_saturation_pressure = QLineEdit()
        form_well.addRow("饱和压力(MPa):", self.edit_saturation_pressure)

        self.edit_heat_coefficient = QLineEdit()
        form_well.addRow("传热系数(W/m·℃):", self.edit_heat_coefficient)

        self.edit_temp_gradient = QLineEdit()
        form_well.addRow("地温梯度(℃/100m):", self.edit_temp_gradient)

        group_well.setLayout(form_well)
        control_layout.addWidget(group_well)

        # 测试数据
        group_test = QGroupBox("测试数据")
        form_test = QFormLayout()

        self.edit_test_production = QLineEdit()
        form_test.addRow("试井产液量(m³/d):", self.edit_test_production)

        self.edit_test_flow_pressure = QLineEdit()
        form_test.addRow("试井流压(MPa):", self.edit_test_flow_pressure)

        self.edit_water_content = QLineEdit()
        form_test.addRow("体积含水率(%):", self.edit_water_content)

        self.edit_oil_density = QLineEdit()
        form_test.addRow("原油密度(kg/m³):", self.edit_oil_density)

        self.edit_water_density = QLineEdit()
        form_test.addRow("地层水密度(kg/m³):", self.edit_water_density)

        self.edit_oil_heat = QLineEdit()
        form_test.addRow("原油比热(J/kg·℃):", self.edit_oil_heat)

        self.edit_water_heat = QLineEdit()
        form_test.addRow("地层水比热(J/kg·℃):", self.edit_water_heat)

        group_test.setLayout(form_test)
        control_layout.addWidget(group_test)

        # 设计参数
        group_design = QGroupBox("设计参数")
        form_design = QFormLayout()

        self.edit_submergence = QLineEdit()
        form_design.addRow("设计沉没度(m):", self.edit_submergence)

        self.edit_design_production = QLineEdit()
        form_design.addRow("设计排量(m³/d):", self.edit_design_production)

        group_design.setLayout(form_design)
        control_layout.addWidget(group_design)

        # 按钮区域
        button_group = QWidget()
        button_layout = QHBoxLayout(button_group)

        self.btn_import = QPushButton("数据导入")
        self.btn_import.clicked.connect(self.import_data)
        button_layout.addWidget(self.btn_import)

        self.btn_temp_curve = QPushButton("井温曲线")
        self.btn_temp_curve.clicked.connect(self.show_temp_curve)
        button_layout.addWidget(self.btn_temp_curve)

        self.btn_viscosity_curve = QPushButton("粘温曲线")
        self.btn_viscosity_curve.clicked.connect(self.show_viscosity_curve)
        button_layout.addWidget(self.btn_viscosity_curve)

        self.btn_ipr_curve = QPushButton("IPR曲线")
        self.btn_ipr_curve.clicked.connect(self.show_ipr_curve)
        button_layout.addWidget(self.btn_ipr_curve)

        control_layout.addWidget(button_group)

        # 右侧图表区域
        self.tab_widget = QTabWidget()
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.tab_widget)

        # 初始化数据
        self.init_data()

    def init_data(self):
        # 初始化抽油机型号数据
        self.model_data = [
            # 型号0
            {
                "strokes": ["0.9", "1.2", "1.5", "1.8"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 50,
                "max_torque": 13,
                "rod_length": 2100,
                "crank_radius": {"0": 380, "1": 500, "2": 620, "3": 740}
            },
            # 型号1
            {
                "strokes": ["1.1", "1.5", "1.9", "2.3", "2.7"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 50,
                "max_torque": 26,
                "rod_length": 2137,
                "crank_radius": {"0": 380, "1": 500, "2": 620, "3": 740, "4": 860}
            },
            # 型号2
            {
                "strokes": ["1.8", "2.2", "2.5"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 60,
                "max_torque": 26,
                "rod_length": 3200,
                "crank_radius": {"0": 670, "1": 990, "2": 150}
            },
            # 型号3
            {
                "strokes": ["2.1", "2.5", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 80,
                "max_torque": 48,
                "rod_length": 3200,
                "crank_radius": {"0": 858, "1": 1013, "2": 1200}
            },
            # 型号4
            {
                "strokes": ["1.8", "2.2", "2.6", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 80,
                "max_torque": 53,
                "rod_length": 3160,
                "crank_radius": {"0": 670, "1": 810, "2": 950, "3": 1090}
            },
            # 型号5
            {
                "strokes": ["1.8", "2.4", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 100,
                "max_torque": 48,
                "rod_length": 3300,
                "crank_radius": {"0": 570, "1": 745, "2": 895}
            },
            # 型号6
            {
                "strokes": ["2.1", "2.5", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 100,
                "max_torque": 53,
                "rod_length": 3200,
                "crank_radius": {"0": 858, "1": 1013, "2": 1200}
            },
            # 型号7
            {
                "strokes": ["1.8", "2.2", "2.6", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 100,
                "max_torque": 53,
                "rod_length": 3380,
                "crank_radius": {"0": 640, "1": 765, "2": 890, "3": 1015}
            },
            # 型号8
            {
                "strokes": ["2.1", "2.5", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 100,
                "max_torque": 53,
                "rod_length": 3200,
                "crank_radius": {"0": 755, "1": 885, "2": 1045}
            },
            # 型号9
            {
                "strokes": ["1.58", "1.88", "2.18"],
                "stroke_times": ["6", "8", "12"],
                "max_load": 110,
                "max_torque": 26,
                "rod_length": 3260,
                "crank_radius": {"0": 780, "1": 922, "2": 1064}
            },
            # 型号10
            {
                "strokes": ["2.85", "3.25", "3.66"],
                "stroke_times": ["8", "12"],
                "max_load": 120,
                "max_torque": 53,
                "rod_length": 4295,
                "crank_radius": {"0": 1074, "1": 1227, "2": 1380}
            },
            # 型号11
            {
                "strokes": ["2.8", "3.8", "4.8"],
                "stroke_times": ["6", "8", "10"],
                "max_load": 120,
                "max_torque": 76,
                "rod_length": 4200,
                "crank_radius": {"0": 800, "1": 1060, "2": 1209}
            },
            # 型号12
            {
                "strokes": ["3", "3.6", "4.3", "5"],
                "stroke_times": ["3", "4", "6"],
                "max_load": 120,
                "max_torque": 74,
                "rod_length": 4640,
                "crank_radius": {"0": 1000, "1": 1200, "2": 1400, "3": 1600}
            },
            # 型号13
            {
                "strokes": ["3.6", "4.2", "4.8"],
                "stroke_times": ["6", "8", "10"],
                "max_load": 140,
                "max_torque": 73,
                "rod_length": 3770,
                "crank_radius": {"0": 990, "1": 1100, "2": 1200}
            },
            # 型号14
            {
                "strokes": ["4", "5"],
                "stroke_times": ["4", "5", "6"],
                "max_load": 140,
                "max_torque": 73,
                "rod_length": 5780,
                "crank_radius": {"0": 970, "1": 1060}
            },
            # 型号15
            {
                "strokes": ["2", "2.5", "3"],
                "stroke_times": ["6", "9", "12"],
                "max_load": 160,
                "max_torque": 300,
                "rod_length": 2100,
                "crank_radius": {"0": 600, "1": 800}
            }
        ]

        # 初始化粘度-温度数据
        self.temp_data = [40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
        self.viscosity_data = [7680, 5820, 3740, 2900, 1720, 1200, 910, 730, 520, 462]

    def on_model_changed(self, index):
        # 清除现有选项
        self.combo_stroke.clear()
        self.combo_stroke_times.clear()

        # 获取当前型号数据
        model = self.model_data[index]

        # 添加冲程选项
        self.combo_stroke.addItems(model["strokes"])
        self.combo_stroke.currentIndexChanged.connect(self.on_stroke_changed)

        # 添加冲次选项
        self.combo_stroke_times.addItems(model["stroke_times"])

        # 设置其他参数
        self.edit_max_load.setText(str(model["max_load"]))
        self.edit_max_torque.setText(str(model["max_torque"]))
        self.edit_rod_length.setText(str(model["rod_length"]))

        # 触发冲程变化事件
        self.on_stroke_changed(0)

    def on_stroke_changed(self, index):
        model_index = self.combo_model.currentIndex()
        if model_index >= 0:
            model = self.model_data[model_index]
            crank_radius = model["crank_radius"].get(str(index), "0")
            self.edit_crank_radius.setText(str(crank_radius))

    def import_data(self):
        # 油层参数
        self.edit_oil_depth.setText("2040")
        self.edit_casing_diameter.setText("190")
        self.edit_tubing_diameter.setText("88.9")
        self.edit_bottom_temp.setText("110")
        self.edit_formation_pressure.setText("15.2")
        self.edit_saturation_pressure.setText("16.1")
        self.edit_heat_coefficient.setText("2.67")
        self.edit_temp_gradient.setText("3.11")

        # 测试数据
        self.edit_test_production.setText("22")
        self.edit_test_flow_pressure.setText("10.3")
        self.edit_water_content.setText("40")
        self.edit_oil_density.setText("981.92")
        self.edit_water_density.setText("1000")
        self.edit_oil_heat.setText("2223.52")
        self.edit_water_heat.setText("4253.77")

        # 设计参数
        self.edit_submergence.setText("240")
        self.edit_design_production.setText("23")

    def show_temp_curve(self):
        # 获取参数
        try:
            fw = float(self.edit_water_content.text()) / 100
            qotest = float(self.edit_test_production.text())
            qo = qotest / 86400
            h = float(self.edit_oil_depth.text())
            t0 = float(self.edit_bottom_temp.text())
            m = float(self.edit_temp_gradient.text())
            Kl = float(self.edit_heat_coefficient.text())
            rouo = float(self.edit_oil_density.text())
            rouw = float(self.edit_water_density.text())
            Mo = float(self.edit_oil_heat.text())
            Mw = float(self.edit_water_heat.text())

            W = (qo * rouo * (1 - fw) * Mo) + (qo * rouw * fw * Mw)
        except:
            return

        # 创建图表
        chart = QChart()
        chart.setTitle("井温曲线")

        # 创建井温曲线
        well_temp_series = QLineSeries()
        well_temp_series.setName("井温曲线")
        well_temp_series.setColor(QColor(0, 0, 255))  # 蓝色

        # 创建地温曲线
        ground_temp_series = QLineSeries()
        ground_temp_series.setName("地温曲线")
        ground_temp_series.setColor(QColor(0, 255, 0))  # 绿色

        # 计算曲线数据
        for L in range(0, int(h) + 1, 1):
            t = W * m / 100 / Kl * (1 - math.exp(-Kl * (h - L) / W)) + (t0 - m / 100 * (h - L))
            if t > t0:
                break
            well_temp_series.append(t, L)

            t_ground = t0 - m / 100 * (h - L)
            ground_temp_series.append(t_ground, L)

        # 添加系列到图表
        chart.addSeries(well_temp_series)
        chart.addSeries(ground_temp_series)

        # 创建坐标轴
        axisX = QValueAxis()
        axisX.setTitleText("温度(℃)")
        axisX.setRange(0, 120)
        axisX.setTickCount(7)
        axisX.setLabelFormat("%.0f")

        axisY = QValueAxis()
        axisY.setTitleText("深度(m)")
        axisY.setRange(0, 2200)
        axisY.setTickCount(12)
        axisY.setLabelFormat("%.0f")

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        well_temp_series.attachAxis(axisX)
        well_temp_series.attachAxis(axisY)
        ground_temp_series.attachAxis(axisX)
        ground_temp_series.attachAxis(axisY)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # 添加到标签页
        self.add_tab(chart_view, "井温曲线")

    def show_viscosity_curve(self):
        # 创建图表
        chart = QChart()
        chart.setTitle("粘温曲线")

        # 创建实测粘度曲线
        measured_series = QLineSeries()
        measured_series.setName("实测粘度")
        measured_series.setColor(QColor(0, 0, 255))  # 蓝色

        # 创建拟合粘度曲线
        fitted_series = QLineSeries()
        fitted_series.setName("拟合粘度")
        fitted_series.setColor(QColor(255, 0, 0))  # 红色

        # 计算拟合参数
        lgt = [math.log10(t) for t in self.temp_data]
        lgu = [math.log10(v) for v in self.viscosity_data]

        x = sum(lgt)
        y = sum(lgu)
        xy = sum([lgt[i] * lgu[i] for i in range(len(lgt))])
        x2 = sum([lg **  2
        for lg in lgt])

        xpj = x / len(lgt)
        ypj = y / len(lgu)

        b = (xy - len(lgt) * xpj * ypj) / (x2 - len(lgt) * (xpj ** 2))
        a = ypj - b * xpj

        # 添加实测数据点
        for i in range(len(self.temp_data)):
            measured_series.append(self.temp_data[i], self.viscosity_data[i] / 80)

        # 添加拟合曲线
        for t in range(40, 86, 1):
            ylf = 10 **  a / (t ** b) / 80
            fitted_series.append(t, ylf)

        # 添加系列到图表
        chart.addSeries(measured_series)
        chart.addSeries(fitted_series)

        # 创建坐标轴
        axisX = QValueAxis()
        axisX.setTitleText("温度(℃)")
        axisX.setRange(30, 90)
        axisX.setTickCount(7)
        axisX.setLabelFormat("%.0f")

        axisY = QValueAxis()
        axisY.setTitleText("粘度(mPa·s)")
        axisY.setRange(0, 100)
        axisY.setTickCount(11)
        axisY.setLabelFormat("%.0f")

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        measured_series.attachAxis(axisX)
        measured_series.attachAxis(axisY)
        fitted_series.attachAxis(axisX)
        fitted_series.attachAxis(axisY)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # 添加到标签页
        self.add_tab(chart_view, "粘温曲线")

    def show_ipr_curve(self):
        # 获取参数
        try:
            qotest = float(self.edit_test_production.text())
            pwftest = float(self.edit_test_flow_pressure.text())
            pr = float(self.edit_formation_pressure.text())
            pb = float(self.edit_saturation_pressure.text())
            qo = float(self.edit_design_production.text())
        except:
            return

        # 计算参数
        Jo = qotest / (pr - pwftest)
        qb = Jo * (pr - pb)
        qc = Jo * pb / 1.8

        # 创建图表
        chart = QChart()
        chart.setTitle("IPR曲线")

        # 创建IPR曲线
        ipr_series = QLineSeries()
        ipr_series.setName("IPR曲线")
        ipr_series.setColor(QColor(0, 255, 0))  # 绿色

        # 计算曲线数据
        for h in range(0, int(pr * 10) + 1, 1):
            pwf = pr - h / 10
            if pwf < (pr - pb):
                q = Jo * (pr - pwf)
            else:
                q = qb + qc * (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb) ** 2)

            ipr_series.append(q * 4, pwf * 10)

        # 添加系列到图表
        chart.addSeries(ipr_series)

        # 创建坐标轴
        axisX = QValueAxis()
        axisX.setTitleText("产液量(m³/d)")
        axisX.setRange(0, 200)
        axisX.setTickCount(11)
        axisX.setLabelFormat("%.0f")

        axisY = QValueAxis()
        axisY.setTitleText("井底流压(MPa)")
        axisY.setRange(0, 170)
        axisY.setTickCount(18)
        axisY.setLabelFormat("%.0f")

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        ipr_series.attachAxis(axisX)
        ipr_series.attachAxis(axisY)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # 添加到标签页
        self.add_tab(chart_view, "IPR曲线")

    def add_tab(self, widget, title):
        # 检查是否已存在相同标题的标签页
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == title:
                self.tab_widget.removeTab(i)
                break

        # 添加新标签页
        self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())