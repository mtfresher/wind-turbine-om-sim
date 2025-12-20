import numpy as np

class BearingTemperatureSimulator:
    """
    风机轴承温度模拟器，使用均值回复随机过程模拟温度变化。
    单位：时间以“分钟”为单位。
    """

    def __init__(self, tau: float, sigma: float, dt: float, mean_temp: float):
        """
        :param tau: 温度向长期均值回复的时间常数（分钟）
        :param sigma: 随机扰动强度，决定温度噪声大小
        :param dt: 时间步长（分钟）
        :param mean_temp: 轴承的平均温度（摄氏度）
        """
        self.tau = tau
        self.sigma = sigma
        self.dt = dt
        self.mean_temp = mean_temp
        self.current_temp = mean_temp

    def step(self) -> float:
        """
        模拟下一个时间步（dt 分钟）的轴承温度。
        :return: 下一时刻的轴承温度
        """
        dW = np.random.normal(0.0, np.sqrt(self.dt))
        drift = -(self.current_temp - self.mean_temp) / self.tau * self.dt
        diffusion = self.sigma * dW

        self.current_temp += drift + diffusion
        return self.current_temp

    def simulate(self, minutes: int) -> np.ndarray:
        """
        按分钟为步长模拟给定时长的轴承温度。
        :param minutes: 总模拟时长（单位：分钟，整数）
        :return: 温度时间序列（numpy 数组，长度为 minutes）
        """
        temps = np.zeros(minutes)
        for i in range(minutes):
            temps[i] = self.step()
        return temps