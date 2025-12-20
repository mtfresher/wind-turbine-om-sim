import numpy as np
import matplotlib.pyplot as plt

class PowerAnalysis:
    """
    风机功率分析类，用于分析风机的功率输出和性能指标。
    """

    def __init__(self, power_data: np.ndarray, wind_speed_data: np.ndarray):
        """
        初始化功率分析类
        :param power_data: 风机功率数据（单位：kW）
        :param wind_speed_data: 风速数据（单位：m/s）
        """
        self.power_data = power_data
        self.wind_speed_data = wind_speed_data

    def calculate_efficiency(self) -> np.ndarray:
        """
        计算风机效率
        :return: 风机效率数组
        """
        # 假设额定功率为2000 kW
        rated_power = 2000.0
        efficiency = self.power_data / rated_power
        return efficiency

    def plot_power_curve(self):
        """
        绘制功率曲线图
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(self.wind_speed_data, self.power_data, color='blue', label='Power Output')
        plt.title('Wind Turbine Power Curve')
        plt.xlabel('Wind Speed (m/s)')
        plt.ylabel('Power Output (kW)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def analyze_performance(self):
        """
        分析风机性能，包括效率和功率曲线
        """
        efficiency = self.calculate_efficiency()
        print("风机效率:", efficiency)
        self.plot_power_curve()