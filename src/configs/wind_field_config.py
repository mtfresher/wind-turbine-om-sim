# 文件: /wind-turbine-om-sim/wind-turbine-om-sim/src/configs/wind_field_config.py

# 风场模拟配置参数
class WindFieldConfig:
    def __init__(self):
        self.mean_wind_speed = 10.0  # 平均风速 (m/s)
        self.wind_speed_variance = 2.0  # 风速方差
        self.mean_wind_direction = 0.0  # 平均风向 (度)
        self.wind_direction_variance = 5.0  # 风向方差
        self.turbulence_intensity = 0.1  # 湍流强度
        self.simulation_duration = 3600  # 模拟持续时间 (秒)
        self.time_step = 1.0  # 时间步长 (秒)

    def __repr__(self):
        return (f"WindFieldConfig(mean_wind_speed={self.mean_wind_speed}, "
                f"wind_speed_variance={self.wind_speed_variance}, "
                f"mean_wind_direction={self.mean_wind_direction}, "
                f"wind_direction_variance={self.wind_direction_variance}, "
                f"turbulence_intensity={self.turbulence_intensity}, "
                f"simulation_duration={self.simulation_duration}, "
                f"time_step={self.time_step})")