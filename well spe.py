import math
from dataclasses import dataclass
from typing import List


@dataclass
class PumpType:
    name: str
    max_load: float  # 最大载荷(kN)
    max_torque: float  # 最大扭矩(kN·m)
    rod_length: float  # 连杆长度(mm)


@dataclass
class PumpParams:
    strokes: List[float]  # 冲程选项(m)
    speeds: List[float]  # 冲次选项(min⁻¹)


# 抽油机型号数据
PUMP_TYPES = [
    PumpType("CYJ5-1.8-18F", 50, 13, 2100),
    PumpType("CYJ7-2.1-26F", 50, 26, 2137),
    # 其他型号数据...
]

# 冲程和冲次选项
PUMP_PARAMS = [
    PumpParams([0.9, 1.2, 1.5, 1.8], [6, 9, 12]),
    PumpParams([1.1, 1.5, 1.9, 2.3, 2.7], [6, 9, 12]),
    # 其他参数数据...
]


class PumpSystem:
    def __init__(self):
        self.selected_type = 0
        self.selected_stroke = 0
        self.selected_speed = 0
        self.crank_radius = 0  # 曲柄半径(mm)
        self.pump_diameter = 44.0  # 默认泵径(mm)

    def select_pump_type(self, index: int):
        """选择抽油机型号"""
        if 0 <= index < len(PUMP_TYPES):
            self.selected_type = index
            print(f"已选择抽油机型号: {PUMP_TYPES[index].name}")
            print(f"最大载荷: {PUMP_TYPES[index].max_load} kN")
            print(f"最大扭矩: {PUMP_TYPES[index].max_torque} kN·m")
            print(f"连杆长度: {PUMP_TYPES[index].rod_length} mm")

    def select_stroke(self, index: int):
        """选择冲程并计算曲柄半径"""
        params = PUMP_PARAMS[self.selected_type]
        if 0 <= index < len(params.strokes):
            self.selected_stroke = index
            stroke = params.strokes[index]
            print(f"已选择冲程: {stroke} m")

            # 曲柄半径计算逻辑 (根据型号和冲程)
            if self.selected_type == 0:
                self.crank_radius = [380, 500, 620, 740][index]
            elif self.selected_type == 1:
                self.crank_radius = [380, 500, 620, 740, 860][index]
            else:
                self.crank_radius = stroke * 200  # 默认计算方式

            print(f"曲柄半径: {self.crank_radius} mm")

    def calculate_pump_diameter(self, design_flow: float = 23.0):
        """计算泵径(mm)

        公式: $D_p = 1000 \times \sqrt{\frac{4Q}{1440 \times s \times n \times \eta \times \pi}}$
        """
        s = PUMP_PARAMS[self.selected_type].strokes[self.selected_stroke]
        n = PUMP_PARAMS[self.selected_type].speeds[self.selected_speed]
        eta = 0.7  # 泵效

        dp = 1000 * math.sqrt(
            (4 * design_flow) / (1440 * s * n * eta * math.pi)
        )
        self.pump_diameter = math.floor(dp)  # 取整

        print(f"计算泵径: {self.pump_diameter} mm")
        return self.pump_diameter

    def calculate_torque(self):
        """计算扭矩(kN·m)

        公式: $M_{max} = \frac{s}{4} \times (P_{max} - P_{min})$
        """
        s = PUMP_PARAMS[self.selected_type].strokes[self.selected_stroke]
        max_load = PUMP_TYPES[self.selected_type].max_load * 0.9  # 估算最大载荷
        min_load = PUMP_TYPES[self.selected_type].max_load * 0.3  # 估算最小载荷

        torque = s / 4 * (max_load - min_load)
        print(f"计算扭矩: {torque:.1f} kN·m")

        # 扭矩校核
        if torque <= PUMP_TYPES[self.selected_type].max_torque:
            print("扭矩校核: 满足要求")
        else:
            print("扭矩校核: 不满足要求")

        return torque

    def calculate_motor_power(self):
        """计算电机功率(kW)

        公式: $N_{max} = \frac{M_{max} \times n}{9.549 \times \eta}$
        """
        torque = self.calculate_torque()
        n = PUMP_PARAMS[self.selected_type].speeds[self.selected_speed]
        eta = 0.9  # 传动效率

        power = torque * n / 9.549 / eta
        print(f"电机最大功率: {power:.1f} kW")
        return power


# 使用示例
if __name__ == "__main__":
    system = PumpSystem()
    system.select_pump_type(0)  # 选择第一种型号
    system.select_stroke(0)  # 选择第一个冲程
    system.calculate_pump_diameter()
    system.calculate_motor_power()