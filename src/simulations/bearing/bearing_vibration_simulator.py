import numpy as np

class BearingVibrationSimulator:
    """
    风机轴承振动模拟器，使用均值回复随机过程模拟“振动速度 RMS（mm/s）”指标。
    时间步长单位：分钟（dt）。
    """

    def __init__(
        self,
        mean_rms: float = 2.0,
        tau: float = 60.0,
        sigma: float = 0.2,
        dt: float = 1.0,
        initial_rms: float | None = None,
    ):
        """
        :param mean_rms: 振动速度 RMS 的长期均值（mm/s），例如 2 mm/s
        :param tau: 向长期均值回复的时间常数（分钟），值越大，变化越慢
        :param sigma: 随机扰动强度（mm/s / sqrt(min)），值越大，波动越大
        :param dt: 时间步长（分钟）
        :param initial_rms: 初始 RMS 值（mm/s），默认等于 mean_rms
        """
        self.mean_rms = mean_rms
        self.tau = tau
        self.sigma = sigma
        self.dt = dt
        self.current_rms = initial_rms if initial_rms is not None else mean_rms

    def step(self) -> float:
        """
        模拟下一个时间步（dt 分钟）的振动速度 RMS（mm/s）。
        采用 Ornstein–Uhlenbeck 类型过程：
        dX = -(X - mean) / tau * dt + sigma * sqrt(dt) * N(0,1)
        :return: 当前振动速度 RMS（mm/s）
        """
        dW = np.random.normal(0.0, np.sqrt(self.dt))
        drift = -(self.current_rms - self.mean_rms) / self.tau * self.dt
        diffusion = self.sigma * dW

        self.current_rms += drift + diffusion

        # RMS 理论上非负，做一个下限截断，避免数值跑到负值
        if self.current_rms < 0.0:
            self.current_rms = 0.0

        return self.current_rms

    def simulate(self, steps: int) -> np.ndarray:
        """
        模拟多步振动速度 RMS。
        :param steps: 模拟步数（以 dt 为步长）
        :return: 振动速度 RMS 时间序列（mm/s）
        """
        vibrations_rms = np.zeros(steps)
        for i in range(steps):
            vibrations_rms[i] = self.step()
        return vibrations_rms