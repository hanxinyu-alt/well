from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class IPRCurveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPR曲线")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 创建图表
        chart = QChart()
        chart.setTitle("IPR曲线")

        # 创建系列
        ipr_series = QLineSeries()
        ipr_series.setName("IPR曲线")

        # 模拟IPR曲线数据
        pr = 16.38  # 地层压力
        pb = 12.52  # 饱和压力
        q_test = 27.7  # 试井产液量
        pwf_test = 8.16  # 试井流压

        # 计算Jo (采液指数)
        Jo = q_test / (pr - pwf_test)

        # 生成曲线数据
        for pwf in [i * 0.1 for i in range(0, int(pr * 10) + 1)]:
            if pwf >= pb:
                q = Jo * (pr - pwf)
            else:
                q = Jo * (pr - pb) + Jo * pb / 1.8 * (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb) ** 2)
            ipr_series.append(q, pwf)

        # 添加到图表
        chart.addSeries(ipr_series)

        # 设置坐标轴
        axis_x = QValueAxis()
        axis_x.setTitleText("产液量(m³/d)")
        axis_x.setRange(0, 50)
        axis_x.setTickCount(6)

        axis_y = QValueAxis()
        axis_y.setTitleText("流压(MPa)")
        axis_y.setRange(0, 17)
        axis_y.setTickCount(9)

        chart.setAxisX(axis_x, ipr_series)
        chart.setAxisY(axis_y, ipr_series)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chart_view)
        self.setLayout(layout)
        self.resize(800, 600)