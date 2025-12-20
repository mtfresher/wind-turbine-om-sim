import numpy as np
import matplotlib.pyplot as plt

class TemperatureSimulator:
    """
    使用均值回复随机过程（Ornstein-Uhlenbeck）模拟自然环境温度随时间的变化（单位：小时）。
    """

    def __init__(
        self,
        tau: float,
        sigma: float,
        dt: float,
        mean_temp: float,
        daily_amp: float = 5.0,
        daily_phase: float = -3.0,
    ):
        """
        :param tau: 温度向长期均值回复的时间常数（小时），越大越平缓
        :param sigma: 随机扰动强度，决定温度噪声大小
        :param dt: 时间步长（小时）
        :param mean_temp: 日平均温度（摄氏度）
        :param daily_amp: 日变化振幅（白天/夜间温差的一半，摄氏度）
        :param daily_phase: 日变化相位（小时偏移，用于控制高温出现在一天中的大致时间）
        """
        self.tau = tau
        self.sigma = sigma
        self.dt = dt
        self.mean_temp = mean_temp
        self.daily_amp = daily_amp
        self.daily_phase = daily_phase

        # 初始化当前温度为均值
        self.current_temp = mean_temp

    def _daily_cycle(self, t_hour: float) -> float:
        """
        日变化项：用简单的正弦函数模拟白天升温、夜间降温。
        :param t_hour: 从起始时刻算起的小时数
        :return: 相对于 mean_temp 的温度偏移量
        """
        return self.daily_amp * np.sin(2 * np.pi * (t_hour + self.daily_phase) / 24.0)

    def step(self, t_hour: float) -> float:
        """
        模拟下一个时间步的温度。
        :param t_hour: 当前时间（从 0 开始计的小时数，用于日变化计算）
        :return: 下一时刻温度
        """
        target_temp = self.mean_temp + self._daily_cycle(t_hour)

        dW = np.random.normal(0.0, np.sqrt(self.dt))
        drift = -(self.current_temp - target_temp) / self.tau * self.dt
        diffusion = self.sigma * dW

        self.current_temp += drift + diffusion
        return self.current_temp

    def simulate(self, hours: int) -> np.ndarray:
        """
        按小时为步长模拟给定时长的环境温度。
        :param hours: 总模拟时长（单位：小时，整数）
        :return: 温度时间序列（numpy 数组，长度为 hours）
        """
        temps = np.zeros(hours)
        for i in range(hours):
            t_hour = i * self.dt
            temps[i] = self.step(t_hour)
        return temps