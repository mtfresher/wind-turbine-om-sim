import numpy as np

class WindTurbinePowerSimulator:
    """
    风机功率和转速模拟器

    功率曲线分段：
    - v < v_in        : P = 0
    - v_in ~ v_rated  : P 按三次多项式平滑上升到额定功率
    - v_rated ~ v_out : P = P_rated
    - v > v_out       : P = 0
    """
    def __init__(
        self,
        v_in: float = 3.0,      # 切入风速 (m/s)
        v_rated: float = 12.0,  # 额定风速 (m/s)
        v_out: float = 25.0,    # 切出风速 (m/s)
        p_rated: float = 2000.0,  # 额定功率 (kW)
        noise_sigma: float = 0.02,  # 功率噪声比例（相对额定功率）
        # 转速相关参数（1 分钟平均转速）
        rpm_min: float = 6.0,      # 最低运行转速 (rpm)
        rpm_rated: float = 15.0,   # 额定转速 (rpm)
        rpm_noise_sigma: float = 0.2,  # 转速噪声 (rpm)
    ):
        self.v_in = v_in
        self.v_rated = v_rated
        self.v_out = v_out
        self.p_rated = p_rated
        self.noise_sigma = noise_sigma

        self.rpm_min = rpm_min
        self.rpm_rated = rpm_rated
        self.rpm_noise_sigma = rpm_noise_sigma

    def _power_curve_ideal(self, v: float) -> float:
        """
        单点：给定风速，计算理想功率（无噪声）
        """
        if v < self.v_in:
            return 0.0
        if v >= self.v_out:
            return 0.0
        if self.v_in <= v < self.v_rated:
            x = (v - self.v_in) / (self.v_rated - self.v_in)
            y = 3 * x**2 - 2 * x**3
            return y * self.p_rated
        return self.p_rated

    def power_from_speed(self, wind_speeds: np.ndarray) -> np.ndarray:
        """
        根据风速序列计算功率序列（带少量随机波动）
        :param wind_speeds: numpy 数组，单位 m/s
        :return: 功率序列，单位 kW
        """
        wind_speeds = np.asarray(wind_speeds)
        ideal_power = np.vectorize(self._power_curve_ideal)(wind_speeds)

        # 添加相对额定功率的小噪声
        noise = np.random.normal(0, self.noise_sigma * self.p_rated, size=ideal_power.shape)
        return ideal_power + noise

    def rpm_from_power(self, power: np.ndarray) -> np.ndarray:
        """
        根据功率序列计算转速序列（带噪声）
        :param power: numpy 数组，单位 kW
        :return: 转速序列，单位 rpm
        """
        rpm = np.clip((power / self.p_rated) * self.rpm_rated, self.rpm_min, self.rpm_rated)
        noise = np.random.normal(0, self.rpm_noise_sigma, size=rpm.shape)
        return rpm + noise