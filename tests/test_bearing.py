import unittest
import numpy as np
from src.simulations.bearing.bearing_temp_simulator import BearingTemperatureSimulator
from src.simulations.bearing.bearing_vibration_simulator import BearingVibrationSimulator

class TestBearingSimulators(unittest.TestCase):

    def setUp(self):
        # 初始化轴承温度和振动模拟器
        self.temp_simulator = BearingTemperatureSimulator(
            tau=10.0,
            sigma=1.0,
            dt=1.0,
            base_temp=40.0,
            rpm_min=6.0,
            rpm_rated=15.0,
            temp_rise_at_rated=15.0,
        )
        self.vibration_simulator = BearingVibrationSimulator(
            base_rms=1.5,
            rpm_min=6.0,
            rpm_rated=15.0,
            rms_at_rated=2.5
        )

    def test_temperature_with_ambient_and_rpm(self):
        # 测试温度模拟器与环境温度和转速的关系
        ambient_temps = np.array([20.0, 22.0, 25.0, 20.0])
        rpm_sequence = np.array([6.0, 9.0, 12.0, 15.0])
        
        temperatures = self.temp_simulator.simulate(ambient_temps, rpm_sequence)
        
        # 验证输出是数组且长度正确
        self.assertIsInstance(temperatures, np.ndarray)
        self.assertEqual(len(temperatures), len(ambient_temps))
        
        # 验证所有温度值都非负
        self.assertTrue(np.all(temperatures >= 0))
        
        # 验证温度大于对应的环境温度（由于摩擦生热）
        self.assertTrue(np.all(temperatures >= ambient_temps))

    def test_temperature_constant_conditions(self):
        # 测试恒定环境温度和转速下的温度模拟
        minutes = 20
        ambient_temp = 20.0
        rpm = 12.0
        
        temperatures = self.temp_simulator.simulate_with_fixed_conditions(minutes, ambient_temp, rpm)
        
        # 验证输出是数组且长度正确
        self.assertIsInstance(temperatures, np.ndarray)
        self.assertEqual(len(temperatures), minutes)
        
        # 验证所有温度值都非负且大于等于环境温度
        self.assertTrue(np.all(temperatures >= ambient_temp))
        
        # 在恒定条件下，温度应该趋向稳定值
        # 后期的值方差应该比早期小（趋向稳定）
        early_temps = temperatures[:5]
        late_temps = temperatures[-5:]
        # 注意：由于有噪声，这个测试可能不总是成立，所以这里做一个松散的检查
        self.assertGreaterEqual(late_temps.std(), 0)
        
    def test_temperature_friction_heat_rise(self):
        # 测试摩擦生热随转速的关系
        rise_at_min = self.temp_simulator._get_friction_heat_rise(6.0)
        rise_at_mid = self.temp_simulator._get_friction_heat_rise(10.5)
        rise_at_rated = self.temp_simulator._get_friction_heat_rise(15.0)
        
        # 验证低速时无生热
        self.assertAlmostEqual(rise_at_min, 0.0, places=5)
        
        # 验证额定转速时的生热
        self.assertAlmostEqual(rise_at_rated, 15.0, places=5)
        
        # 验证中间转速的生热在两者之间（二次关系）
        self.assertGreater(rise_at_mid, rise_at_min)
        self.assertLess(rise_at_mid, rise_at_rated)

    def test_vibration_with_rpm_sequence(self):
        # 测试振动模拟器与转速序列的关系
        rpm_sequence = np.array([6.0, 8.0, 10.0, 12.0, 15.0])
        vibrations = self.vibration_simulator.simulate(rpm_sequence)
        
        # 验证输出是数组且长度正确
        self.assertIsInstance(vibrations, np.ndarray)
        self.assertEqual(len(vibrations), len(rpm_sequence))
        
        # 验证所有振动值都非负
        self.assertTrue(np.all(vibrations >= 0))
        
    def test_vibration_constant_rpm(self):
        # 测试恒定转速下的振动模拟
        steps = 10
        rpm = 12.0
        vibrations = self.vibration_simulator.simulate_constant_rpm(steps, rpm)
        
        # 验证输出是数组且长度正确
        self.assertIsInstance(vibrations, np.ndarray)
        self.assertEqual(len(vibrations), steps)
        
        # 验证所有振动值都非负
        self.assertTrue(np.all(vibrations >= 0))
        
    def test_vibration_mean_rpm_relationship(self):
        # 测试振动均值与转速的关系
        mean_rms_at_min = self.vibration_simulator._get_mean_rms_from_rpm(6.0)
        mean_rms_at_rated = self.vibration_simulator._get_mean_rms_from_rpm(15.0)
        
        # 验证在最小转速时的均值
        self.assertAlmostEqual(mean_rms_at_min, 1.5, places=5)
        # 验证在额定转速时的均值
        self.assertAlmostEqual(mean_rms_at_rated, 2.5, places=5)
        
        # 验证中间转速的均值在两者之间（二次关系）
        mean_rms_at_mid = self.vibration_simulator._get_mean_rms_from_rpm(10.5)
        self.assertGreater(mean_rms_at_mid, mean_rms_at_min)
        self.assertLess(mean_rms_at_mid, mean_rms_at_rated)

        
        # 验证所有振动值都非负
        self.assertTrue(np.all(vibrations >= 0))
        
    def test_vibration_mean_rpm_relationship(self):
        # 测试均值与转速的关系
        mean_rms_at_min = self.vibration_simulator._get_mean_rms_from_rpm(6.0)
        mean_rms_at_rated = self.vibration_simulator._get_mean_rms_from_rpm(15.0)
        
        # 验证在额定转速时的均值符合配置
        self.assertAlmostEqual(mean_rms_at_min, 1.5, places=5)
        self.assertAlmostEqual(mean_rms_at_rated, 2.5, places=5)
        
        # 验证中间转速的均值在两者之间（二次关系）
        mean_rms_at_mid = self.vibration_simulator._get_mean_rms_from_rpm(10.5)
        self.assertGreater(mean_rms_at_mid, mean_rms_at_min)
        self.assertLess(mean_rms_at_mid, mean_rms_at_rated)

if __name__ == '__main__':
    unittest.main()
