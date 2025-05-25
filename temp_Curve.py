from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt


class TempCurveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("井温曲线")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 创建图表
        chart = QChart()
        chart.setTitle("井温和地温曲线")

        # 创建系列
        well_temp_series = QLineSeries()
        well_temp_series.setName("井温曲线")
        earth_temp_series = QLineSeries()
        earth_temp_series.setName("地温曲线")

        # 添加模拟数据
        for i in range(0, 2201, 100):
            well_temp = 80 + i * 0.02  # 模拟井温
            earth_temp = 80 + i * 0.015  # 模拟地温
            well_temp_series.append(well_temp, i)
            earth_temp_series.append(earth_temp, i)

        # 添加到图表
        chart.addSeries(well_temp_series)
        chart.addSeries(earth_temp_series)

        # 设置坐标轴
        axis_x = QValueAxis()
        axis_x.setTitleText("温度(℃)")
        axis_x.setRange(0, 120)
        axis_x.setTickCount(7)
        axis_x.setLabelFormat("%.1f")

        axis_y = QValueAxis()
        axis_y.setTitleText("深度(m)")
        axis_y.setRange(0, 2200)
        axis_y.setTickCount(12)
        axis_y.setLabelFormat("%d")

        chart.setAxisX(axis_x, well_temp_series)
        chart.setAxisY(axis_y, well_temp_series)
        chart.setAxisX(axis_x, earth_temp_series)
        chart.setAxisY(axis_y, earth_temp_series)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        self.setLayout(layout)
        self.resize(800, 600)