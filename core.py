class CalculatorCore:
    def __init__(self):
        self.memory = 0
        self.history = []

    def calculate(self, expression):
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            raise ValueError(f"计算错误: {str(e)}")