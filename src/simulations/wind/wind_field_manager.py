import numpy as np
from .wind_speed_simu import WindSpeedSimulator

class WindFieldManager:
    def __init__(self, wind_speed_simulator: WindSpeedSimulator | None = None):
        """
        初始化风场管理器
        :param wind_speed_simulator: 风速+风向模拟器实例，不传则使用默认参数创建
        """
        self.wind_speed_simulator = wind_speed_simulator or WindSpeedSimulator()

    def simulate(self, steps: int) -> tuple[np.ndarray, np.ndarray]:
        """
        模拟给定步数的风速和风向角
        :param steps: 模拟步数
        :return: (风速时间序列, 风向角时间序列)
        """
        wind_speeds = np.zeros(steps)
        wind_dirs = np.zeros(steps)

        for i in range(steps):
            speed, direction = self.wind_speed_simulator.step()
            wind_speeds[i] = speed
            wind_dirs[i] = direction

        return wind_speeds, wind_dirs

    def get_current_conditions(self) -> tuple[float, float]:
        """
        获取当前风速和风向角
        :return: (当前风速, 当前风向角)
        """
        return self.wind_speed_simulator.wind_speed, self.wind_speed_simulator.wind_dir