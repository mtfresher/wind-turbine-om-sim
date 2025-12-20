import numpy as np

class WindSpeedSimulator:
    def __init__(self, tau=5.0, sigma=2.0, dt=0.1, mean_wind=10.0,
                 tau_dir=30.0, sigma_dir=5.0, mean_dir=0.0):
        """
        初始化风速模拟器
        :param tau: 一阶惯性时间常数（风速）
        :param sigma: 随机扰动强度（风速）
        :param dt: 时间步长(秒)
        :param mean_wind: 平均风速
        :param tau_dir: 一阶惯性时间常数（风向角）
        :param sigma_dir: 随机扰动强度（风向角，单位：度）
        :param mean_dir: 平均风向角（单位：度，可理解为主风向）
        """
        self.tau = tau
        self.sigma = sigma
        self.dt = dt
        self.mean_wind = mean_wind

        # 风向角相关参数
        self.tau_dir = tau_dir
        self.sigma_dir = sigma_dir
        self.mean_dir = mean_dir

        # 状态初始化
        self.wind_speed = mean_wind
        self.wind_dir = mean_dir  # 当前风向角，单位：度

    def _step_speed(self):
        """
        模拟单步风速（Ornstein–Uhlenbeck 过程）
        """
        dw = - (self.wind_speed - self.mean_wind) / self.tau * self.dt
        dw += self.sigma * np.sqrt(self.dt) * np.random.normal()
        self.wind_speed += dw
        return self.wind_speed

    def _wrap_angle(self, angle_deg):
        """
        将角度归一化到 [-180, 180) 区间，防止数值发散
        """
        angle_deg = (angle_deg + 180.0) % 360.0 - 180.0
        return angle_deg

    def _step_direction(self):
        """
        模拟单步风向角，使用一阶惯性 + 随机扰动
        风向变化通常比风速慢、幅度小，以增强真实感
        """
        # 差值按最小角度差来算（考虑绕圈）
        diff = self._wrap_angle(self.wind_dir - self.mean_dir)

        dtheta = - diff / self.tau_dir * self.dt
        dtheta += self.sigma_dir * np.sqrt(self.dt) * np.random.normal()

        self.wind_dir += dtheta
        self.wind_dir = self._wrap_angle(self.wind_dir)
        return self.wind_dir

    def step(self):
        """
        模拟单步：返回当前风速和风向角
        :return: (风速, 风向角[度])
        """
        speed = self._step_speed()
        direction = self._step_direction()
        return speed, direction

    def simulate(self, steps):
        """
        模拟多步风速和风向角
        :param steps: 模拟步数
        :return: (风速时间序列, 风向角时间序列)
        """
        wind_speeds = []
        wind_dirs = []
        for _ in range(steps):
            speed, direction = self.step()
            wind_speeds.append(speed)
            wind_dirs.append(direction)
        return wind_speeds, wind_dirs