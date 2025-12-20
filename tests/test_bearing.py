import unittest
from src.simulations.bearing.bearing_temp_simulator import BearingTempSimulator
from src.simulations.bearing.bearing_vibration_simulator import BearingVibrationSimulator

class TestBearingSimulators(unittest.TestCase):

    def setUp(self):
        # 初始化轴承温度和振动模拟器
        self.temp_simulator = BearingTempSimulator()
        self.vibration_simulator = BearingVibrationSimulator()

    def test_temperature_simulation(self):
        # 测试温度模拟器的输出
        temperature = self.temp_simulator.simulate()
        self.assertIsInstance(temperature, float)
        self.assertGreaterEqual(temperature, 0)  # 假设温度不能为负

    def test_vibration_simulation(self):
        # 测试振动模拟器的输出
        vibration = self.vibration_simulator.simulate()
        self.assertIsInstance(vibration, float)
        self.assertGreaterEqual(vibration, 0)  # 假设振动值不能为负

if __name__ == '__main__':
    unittest.main()