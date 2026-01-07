import numpy as np

class BearingVibrationSimulator:
    """
    风机轴承振动模拟器，使用均值回复随机过程模拟“振动速度 RMS（mm/s）”指标。    振动与转速相关：转速越高，轴承受力越大，振动越剧烈（二次关系）。    时间步长单位：分钟（dt）。
    """

    def __init__(
        self,
        rpm_min: float = 6.0,
        rpm_rated: float = 15.0,
        base_rms: float = 1.5,
        rms_at_rated: float = 2.5,
        tau: float = 60.0,
        sigma: float = 0.2,
        dt: float = 1.0,
        initial_rms: float | None = None,
    ):
        """
        :param base_rms: 基础振动 RMS（最小转速时的值）（mm/s）
        :param rpm_min: 最小运行转速（rpm），对应基础振动
        :param rpm_rated: 额定转速（rpm）
        :param rms_at_rated: 额定转速时的振动 RMS（mm/s）
        :param tau: 向均值回复的时间常数（分钟），值越大，变化越慢
        :param sigma: 随机扰动强度（mm/s / sqrt(min)），值越大，波动越大
        :param dt: 时间步长（分钟）
        :param initial_rms: 初始 RMS 值（mm/s），默认等于 base_rms
        """
        self.base_rms = base_rms
        self.rpm_min = rpm_min
        self.rpm_rated = rpm_rated
        self.rms_at_rated = rms_at_rated
        self.tau = tau
        self.sigma = sigma
        self.dt = dt
        self.current_rms = initial_rms if initial_rms is not None else base_rms
        
        # 计算转速-振动的映射系数
        self.rpm_range = self.rpm_rated - self.rpm_min
        self.rms_range = self.rms_at_rated - self.base_rms

    def _get_mean_rms_from_rpm(self, rpm: float) -> float:
        """
        根据转速计算对应的平均振动 RMS。
        使用二次函数模型：RMS(rpm) = base_rms + rms_range * ((rpm - rpm_min) / rpm_range)^2
        这样可以更真实地反映高转速时振动增长快的特点。
        
        :param rpm: 当前转速（rpm）
        :return: 对应的平均振动 RMS（mm/s）
        """
        if rpm <= self.rpm_min:
            return self.base_rms
        if rpm >= self.rpm_rated:
            return self.rms_at_rated
        
        # 二次多项式：振动随转速的平方增长
        x = (rpm - self.rpm_min) / self.rpm_range
        mean_rms = self.base_rms + self.rms_range * (x ** 2)
        return mean_rms

    def step(self, rpm: float) -> float:
        """
        模拟下一个时间步（dt 分钟）的振动速度 RMS（mm/s）。
        采用 Ornstein–Uhlenbeck 类型过程，但均值随转速动态变化：
        dX = -(X - mean_rms(rpm)) / tau * dt + sigma * sqrt(dt) * N(0,1)
        
        :param rpm: 当前时刻的转速（rpm）
        :return: 当前振动速度 RMS（mm/s）
        """
        # 根据实时转速获取均值
        mean_rms = self._get_mean_rms_from_rpm(rpm)
        
        dW = np.random.normal(0.0, np.sqrt(self.dt))
        drift = -(self.current_rms - mean_rms) / self.tau * self.dt
        diffusion = self.sigma * dW

        self.current_rms += drift + diffusion

        # RMS 理论上非负，做一个下限截断，避免数值跑到负值
        if self.current_rms < 0.0:
            self.current_rms = 0.0

        return self.current_rms

    def simulate(self, rpm_sequence: np.ndarray) -> np.ndarray:
        """
        模拟多步振动速度 RMS，考虑实时的转速变化。
        
        :param rpm_sequence: 转速序列（分钟级），长度为模拟步数
        :return: 振动速度 RMS 时间序列（mm/s）
        """
        rpm_sequence = np.asarray(rpm_sequence)
        steps = len(rpm_sequence)
        vibrations_rms = np.zeros(steps)
        
        for i in range(steps):
            vibrations_rms[i] = self.step(rpm_sequence[i])
        
        return vibrations_rms

    def simulate_constant_rpm(self, steps: int, rpm: float) -> np.ndarray:
        """
        模拟在恒定转速下的多步振动速度 RMS（向后兼容）。
        
        :param steps: 模拟步数（以 dt 为步长）
        :param rpm: 恒定转速（rpm）
        :return: 振动速度 RMS 时间序列（mm/s）
        """
        rpm_sequence = np.full(steps, rpm)
        return self.simulate(rpm_sequence)