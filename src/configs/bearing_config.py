# 风机轴承模拟配置参数

class BearingConfig:
    def __init__(self, 
                 bearing_temp_mean: float = 70.0,  # 轴承温度均值（摄氏度）
                 bearing_temp_sigma: float = 2.0,   # 轴承温度噪声强度（摄氏度）
                 bearing_vibration_mean: float = 0.1,  # 轴承振动均值（g）
                 bearing_vibration_sigma: float = 0.01,  # 轴承振动噪声强度（g）
                 bearing_life_hours: int = 20000):  # 轴承预期寿命（小时）
        self.bearing_temp_mean = bearing_temp_mean
        self.bearing_temp_sigma = bearing_temp_sigma
        self.bearing_vibration_mean = bearing_vibration_mean
        self.bearing_vibration_sigma = bearing_vibration_sigma
        self.bearing_life_hours = bearing_life_hours

# 示例配置
bearing_config = BearingConfig()