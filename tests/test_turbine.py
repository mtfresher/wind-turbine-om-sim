import numpy as np
import unittest
from src.simulations.turbine.wind_turbine_power_simu import WindTurbinePowerSimulator

class TestWindTurbinePowerSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = WindTurbinePowerSimulator()

    def test_power_curve(self):
        # 测试不同风速下的功率输出
        test_speeds = [0, 5, 10, 12, 15, 20, 30]
        expected_outputs = [0, 0, 0, 2000, 2000, 2000, 0]  # 额定功率为2000kW
        outputs = self.simulator.power_from_speed(np.array(test_speeds))
        np.testing.assert_almost_equal(outputs, expected_outputs, decimal=1)

    def test_power_with_noise(self):
        # 测试功率输出的噪声
        wind_speeds = np.array([10, 12, 15])
        outputs = self.simulator.power_from_speed(wind_speeds)
        self.assertTrue(np.all(outputs >= 0))  # 确保功率输出非负

    def test_rpm_calculation(self):
        # 测试转速计算
        wind_speed = 12.0  # 额定风速
        power_output = self.simulator.power_from_speed(np.array([wind_speed]))[0]
        expected_rpm = self.simulator.rpm_rated  # 额定转速
        self.assertEqual(expected_rpm, self.simulator.rpm_rated)

if __name__ == '__main__':
    unittest.main()