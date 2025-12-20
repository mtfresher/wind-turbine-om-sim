import numpy as np

class HealthIndexCalculator:
    """
    风机健康指数计算器
    """

    def __init__(self, power_data: np.ndarray, temperature_data: np.ndarray, vibration_data: np.ndarray):
        """
        初始化健康指数计算器
        :param power_data: 风机功率数据（单位：kW）
        :param temperature_data: 风机轴承温度数据（单位：°C）
        :param vibration_data: 风机振动数据（单位：g）
        """
        self.power_data = power_data
        self.temperature_data = temperature_data
        self.vibration_data = vibration_data

    def calculate_health_index(self) -> float:
        """
        计算风机健康指数
        健康指数的计算方式可以根据具体需求进行调整
        假设健康指数 = 功率因子 - 温度因子 - 振动因子
        """
        power_factor = np.mean(self.power_data) / np.max(self.power_data)
        temperature_factor = np.mean(self.temperature_data) / 100.0  # 假设100°C为临界温度
        vibration_factor = np.mean(self.vibration_data) / 5.0  # 假设5g为临界振动值

        health_index = power_factor - temperature_factor - vibration_factor
        return max(0.0, min(1.0, health_index))  # 健康指数限制在0到1之间

    def get_health_status(self) -> str:
        """
        获取风机健康状态
        :return: 健康状态描述
        """
        health_index = self.calculate_health_index()
        if health_index > 0.8:
            return "健康"
        elif health_index > 0.5:
            return "警告"
        else:
            return "故障"