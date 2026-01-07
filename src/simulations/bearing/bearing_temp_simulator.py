import numpy as np

class BearingTemperatureSimulator:
    """
    风机轴承温度模拟器，考虑转速、环境温度、摩擦生热和散热过程。
    使用改进的热传导模型：
    dT/dt = (T_env + T_friction_rise(rpm) - T) / tau + sigma * noise
    时间步长单位：分钟
    """

    def __init__(
        self,
        tau: float = 10.0,
        sigma: float = 1.0,
        dt: float = 1.0,
        base_temp: float = 40.0,
        rpm_min: float = 6.0,
        rpm_rated: float = 15.0,
        temp_rise_at_rated: float = 15.0,
        convection_coeff: float = 0.5,
    ):
        """
        :param tau: 温度向均值回复的时间常数（分钟），模拟热惯性
        :param sigma: 随机扰动强度，决定温度波动大小
        :param dt: 时间步长（分钟）
        :param base_temp: 停机状态下轴承的基础温度（等于环境温度）
        :param rpm_min: 最小运行转速（rpm）
        :param rpm_rated: 额定运行转速（rpm）
        :param temp_rise_at_rated: 额定转速下相对环境温度的温升（°C）
        :param convection_coeff: 冷却系数（越大散热越快），范围通常 0.3~1.0
        """
        self.tau = tau
        self.sigma = sigma
        self.dt = dt
        self.base_temp = base_temp
        self.rpm_min = rpm_min
        self.rpm_rated = rpm_rated
        self.temp_rise_at_rated = temp_rise_at_rated
        self.convection_coeff = convection_coeff
        
        self.current_temp = base_temp
        
    def _get_friction_heat_rise(self, rpm: float) -> float:
        """
        根据转速计算摩擦生热导致的温升。
        使用二次关系：ΔT_friction(rpm) = temp_rise_at_rated * ((rpm - rpm_min) / (rpm_rated - rpm_min))^2
        这符合物理规律：摩擦力与转速平方成正比
        
        :param rpm: 当前转速（rpm）
        :return: 摩擦生热导致的温升（°C）
        """
        if rpm <= self.rpm_min:
            return 0.0
        if rpm >= self.rpm_rated:
            return self.temp_rise_at_rated
        
        # 二次多项式关系：生热随转速的平方增长
        x = (rpm - self.rpm_min) / (self.rpm_rated - self.rpm_min)
        temp_rise = self.temp_rise_at_rated * (x ** 2)
        return temp_rise

    def step(self, ambient_temp: float, rpm: float) -> float:
        """
        模拟下一个时间步的轴承温度。
        物理模型：
        - 轴承温度 = 环境温度 + 摩擦生热温升
        - 实际温度通过热传导过程逐步向这个目标温度靠近
        - 用 Ornstein-Uhlenbeck 过程模拟温度的随机波动
        
        dT = ((T_ambient + ΔT_friction(rpm)) - T_current) / tau * dt + sigma * sqrt(dt) * N(0,1)
        
        :param ambient_temp: 环境温度（°C）
        :param rpm: 当前转速（rpm）
        :return: 当前轴承温度（°C）
        """
        # 计算目标温度 = 环境温度 + 摩擦生热温升
        friction_rise = self._get_friction_heat_rise(rpm)
        target_temp = ambient_temp + friction_rise
        
        # Ornstein-Uhlenbeck 过程：温度向目标温度回复
        dW = np.random.normal(0.0, np.sqrt(self.dt))
        drift = (target_temp - self.current_temp) / self.tau * self.dt
        diffusion = self.sigma * dW
        
        self.current_temp += drift + diffusion
        
        # 施加物理约束：温度不能低于环境温度
        if self.current_temp < ambient_temp:
            self.current_temp = ambient_temp
        
        return self.current_temp

    def simulate(
        self,
        ambient_temps: np.ndarray,
        rpm_sequence: np.ndarray,
        minutes: int | None = None,
    ) -> np.ndarray:
        """
        模拟轴承温度随时间变化。
        
        :param ambient_temps: 环境温度序列（°C），长度为 steps 或 标量
        :param rpm_sequence: 转速序列（rpm），长度为 steps 或 标量
        :param minutes: 如果传入标量，指定模拟分钟数（向后兼容）
        :return: 温度时间序列（numpy 数组）
        """
        ambient_temps = np.asarray(ambient_temps)
        rpm_sequence = np.asarray(rpm_sequence)
        
        # 处理向后兼容的调用方式：单个标量值
        if ambient_temps.ndim == 0 and rpm_sequence.ndim == 0:
            if minutes is None:
                raise ValueError("当传入标量时必须指定 minutes 参数")
            ambient_temps = np.full(minutes, ambient_temps.item())
            rpm_sequence = np.full(minutes, rpm_sequence.item())
        elif ambient_temps.ndim == 0:
            ambient_temps = np.full(len(rpm_sequence), ambient_temps.item())
        elif rpm_sequence.ndim == 0:
            rpm_sequence = np.full(len(ambient_temps), rpm_sequence.item())
        
        steps = len(ambient_temps)
        temps = np.zeros(steps)
        
        for i in range(steps):
            temps[i] = self.step(ambient_temps[i], rpm_sequence[i])
        
        return temps

    def simulate_with_fixed_conditions(
        self,
        minutes: int,
        ambient_temp: float,
        rpm: float,
    ) -> np.ndarray:
        """
        在恒定的环境温度和转速下模拟轴承温度（向后兼容）。
        
        :param minutes: 模拟时长（分钟）
        :param ambient_temp: 恒定的环境温度（°C）
        :param rpm: 恒定的转速（rpm）
        :return: 温度时间序列
        """
        ambient_temps = np.full(minutes, ambient_temp)
        rpm_sequence = np.full(minutes, rpm)
        return self.simulate(ambient_temps, rpm_sequence)
