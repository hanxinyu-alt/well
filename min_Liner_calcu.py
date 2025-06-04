import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QLineEdit,
                             QLabel, QPushButton)


class LogLinearRegressionCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('温度-粘度对数线性回归计算器')
        self.setGeometry(300, 300, 800, 200)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # 温度输入行
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("温度(℃):"))
        self.temp_inputs = []
        for day in range(1, 10):
            edit = QLineEdit()
            edit.setPlaceholderText(f"第{day}组")
            temp_layout.addWidget(edit)
            self.temp_inputs.append(edit)

        # 湿度输入行
        humidity_layout = QHBoxLayout()
        humidity_layout.addWidget(QLabel("粘度(mpa*s):"))
        self.humidity_inputs = []
        for _ in range(9):
            edit = QLineEdit()
            humidity_layout.addWidget(edit)
            self.humidity_inputs.append(edit)

        # 计算按钮
        calc_btn = QPushButton("计算回归方程")
        calc_btn.clicked.connect(self.calculate_regression)

        # 结果显示
        self.result_label = QLabel("回归方程将显示在这里")
        self.result_label.setStyleSheet("font-size: 16px;")

        # 布局组装
        main_layout.addLayout(temp_layout)
        main_layout.addLayout(humidity_layout)
        main_layout.addWidget(calc_btn)
        main_layout.addWidget(self.result_label)
        central_widget.setLayout(main_layout)

    def calculate_regression(self):
        try:
            # 获取输入数据并转换为对数
            X = [np.log10(float(edit.text())) for edit in self.temp_inputs if edit.text()]
            Y = [np.log10(float(edit.text())) for edit in self.humidity_inputs if edit.text()]

            if len(X) != len(Y) or len(X) < 2:
                self.result_label.setText("需要至少2组完整数据")
                return

            # 最小二乘法计算回归系数
            X_arr, Y_arr = np.array(X), np.array(Y)
            n = len(X_arr)
            sum_x = np.sum(X_arr)
            sum_y = np.sum(Y_arr)
            sum_xy = np.sum(X_arr * Y_arr)
            sum_x2 = np.sum(X_arr ** 2)

            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
            intercept = (sum_y - slope * sum_x) / n

            # 显示结果
            equation = f"lg(u) = {slope:.4f} × lg(t) + {intercept:.4f}"
            self.result_label.setText(f"回归方程: {equation}\n(即u = {10 ** intercept:.4f} × t^{slope:.4f})")

        except ValueError:
            self.result_label.setText("请输入有效的正数(对数运算需要正数)")
        except Exception as e:
            self.result_label.setText(f"计算错误: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LogLinearRegressionCalculator()
    window.show()
    sys.exit(app.exec_())
