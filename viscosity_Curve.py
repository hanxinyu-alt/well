from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QScatterSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class ViscosityCurveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("粘温曲线")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 创建图表
        chart = QChart()
        chart.setTitle("粘温曲线")

        # 创建系列
        theory_series = QLineSeries()
        theory_series.setName("理论曲线")
        actual_series = QScatterSeries()
        actual_series.setName("实测数据")
        actual_series.setMarkerSize(8)

        # 添加模拟数据
        temperatures = [40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
        viscosities = [6819, 4514, 2484, 1758, 1257, 840, 632, 421, 323, 254]

        for temp, visc in zip(temperatures, viscosities):
            actual_series.append(temp, visc / 80)  # 除以80以匹配VB中的比例

        # 理论曲线 (模拟)
        for temp in range(30, 91):
            visc = 10000 / (temp **  1.5)  # 简单模拟理论关系
            theory_series.append(temp, visc)

        # 添加到图表
        chart.addSeries(theory_series)
        chart.addSeries(actual_series)

        # 设置坐标轴
        axis_x = QValueAxis()
        axis_x.setTitleText("温度(℃)")
        axis_x.setRange(30, 90)
        axis_x.setTickCount(7)

        axis_y = QValueAxis()
        axis_y.setTitleText("粘度(mPa·s)")
        axis_y.setRange(0, 90)
        axis_y.setTickCount(10)

        chart.setAxisX(axis_x, theory_series)
        chart.setAxisY(axis_y, theory_series)
        chart.setAxisX(axis_x, actual_series)
        chart.setAxisY(axis_y, actual_series)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        self.setLayout(layout)
        self.resize(800, 600)