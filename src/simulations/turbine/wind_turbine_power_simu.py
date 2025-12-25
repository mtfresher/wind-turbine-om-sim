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
        # 转动惯性参数
        time_constant: float = 10.0,  # 时间常数 (s) 越小惯性越小，越大惯性越大
        max_ramp_rate: float = 50.0,  # 最大斜坡率 (kW/s) 功率变化率限制
    ):
        self.v_in = v_in
        self.v_rated = v_rated
        self.v_out = v_out
        self.p_rated = p_rated
        self.noise_sigma = noise_sigma

        self.rpm_min = rpm_min
        self.rpm_rated = rpm_rated
        self.rpm_noise_sigma = rpm_noise_sigma
        
        # 转动惯性参数
        self.time_constant = time_constant
        self.max_ramp_rate = max_ramp_rate

    def _power_curve_ideal(self, v: float) -> float:
        """
        单点：给定风速，计算理想功率（无噪声）
        P = P_rated × (3x² - 2x³), 其中 x = (v-v_in)/(v_rated-v_in)
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
        根据风速序列计算功率序列（带转动惯性和斜坡率限制）
        :param wind_speeds: numpy 数组，单位 m/s
        :return: 功率序列，单位 kW
        """
        wind_speeds = np.asarray(wind_speeds)
        # 计算理想功率
        ideal_power = np.vectorize(self._power_curve_ideal)(wind_speeds)

        # 应用转动惯性滤波（一阶延迟系统）
        # P(n) = P(n-1) + (P_ideal(n) - P(n-1)) * (dt / (tau + dt))
        # 当 dt << tau 时，功率变化缓慢；当 dt >> tau 时，立即响应
        power_filtered = self._apply_inertia_filter(ideal_power)

        # 应用斜坡率限制（防止功率变化过快）
        power_limited = self._apply_ramp_rate_limit(power_filtered)

        # 添加相对较小的噪声（在平滑后）
        noise = np.random.normal(0, self.noise_sigma * self.p_rated, size=power_limited.shape)
        power = power_limited + noise
        
        # 功率不能为负，确保物理意义
        return np.maximum(0.0, power)

    def _apply_inertia_filter(self, ideal_power: np.ndarray) -> np.ndarray:
        """
        应用一阶低通滤波器模拟风机的转动惯性
        使用递推公式：y(n) = y(n-1) + (x(n) - y(n-1)) * alpha
        其中 alpha = dt / (tau + dt), tau 为时间常数
        
        假设采样间隔 dt = 1 秒
        """
        dt = 1.0  # 假设秒级采样
        alpha = dt / (self.time_constant + dt)
        
        filtered = np.zeros_like(ideal_power)
        filtered[0] = ideal_power[0]
        
        for i in range(1, len(ideal_power)):
            filtered[i] = filtered[i-1] + (ideal_power[i] - filtered[i-1]) * alpha
        
        return filtered

    def _apply_ramp_rate_limit(self, power: np.ndarray) -> np.ndarray:
        """
        应用功率变化率限制（斜坡率限制）
        防止功率在相邻时刻变化超过最大斜坡率
        
        假设采样间隔 dt = 1 秒
        """
        dt = 1.0  # 秒级采样
        max_delta = self.max_ramp_rate * dt  # 单步最大变化量
        
        limited = np.zeros_like(power)
        limited[0] = power[0]
        
        for i in range(1, len(power)):
            delta = power[i] - limited[i-1]
            # 限制变化量在 [-max_delta, max_delta] 范围内
            delta = np.clip(delta, -max_delta, max_delta)
            limited[i] = limited[i-1] + delta
        
        return limited

    def rpm_from_power(self, power: np.ndarray) -> np.ndarray:
        """
        根据功率序列计算转速序列（带噪声）
        :param power: numpy 数组，单位 kW
        :return: 转速序列，单位 rpm
        """
        rpm = np.clip((power / self.p_rated) * self.rpm_rated, self.rpm_min, self.rpm_rated)
        noise = np.random.normal(0, self.rpm_noise_sigma, size=rpm.shape)
        rpm = rpm + noise
        # 转速也不能为负，确保物理意义
        return np.clip(rpm, self.rpm_min, self.rpm_rated)