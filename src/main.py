import numpy as np
import matplotlib.pyplot as plt
from simulations.wind.wind_field_manager import WindFieldManager
from simulations.wind.wind_speed_simu import WindSpeedSimulator
from simulations.environment.temperature_simulator import TemperatureSimulator
from simulations.turbine.wind_turbine_power_simu import WindTurbinePowerSimulator
from simulations.bearing.bearing_temp_simulator import BearingTemperatureSimulator
from simulations.bearing.bearing_vibration_simulator import BearingVibrationSimulator

def save_csv(wind_speeds, wind_dirs, wind_speeds_min_average, turbine_power_min, turbine_rpm_min, bearing_temperatures, bearing_vibrations, wind_speeds_hour_average, turbine_power_hour, turbine_rpm_hour, temperatures, turbine_power_sec, turbine_rpm_sec):
    import pandas as pd

    # ========== 秒级 ==========
    df_sec = pd.DataFrame({
        "sec_id": np.arange(len(wind_speeds)),
        "wind_speed": wind_speeds,
        "wind_dir": wind_dirs,
        "power_kw": turbine_power_sec,
        "rpm": turbine_rpm_sec,
    })
    df_sec.to_csv("wind_second.csv", index=False)

    # ========== 分钟级 ==========
    df_min = pd.DataFrame({
        "min_id": np.arange(len(wind_speeds_min_average)),
        "wind_speed_avg": wind_speeds_min_average,
        "power_kw": turbine_power_min,
        "rpm": turbine_rpm_min,
        "bearing_temp": bearing_temperatures,
        "bearing_vibration": bearing_vibrations,
    })
    df_min.to_csv("turbine_minute.csv", index=False)

    # ========== 小时级 ==========
    df_hour = pd.DataFrame({
        "hour_id": np.arange(len(wind_speeds_hour_average)),
        "wind_speed_avg": wind_speeds_hour_average,
        "power_kw": turbine_power_hour,
        "rpm": turbine_rpm_hour,
        "ambient_temp": temperatures,
    })
    df_hour.to_csv("hourly.csv", index=False)


def main():
    # # 600W 风机模拟参数
    # v_in = 2.0      # 切入风速 (m/s)
    # v_rated = 13.0  # 额定风速 (m/s
    # v_out = 50.0    # 切出风速 (m/s)
    # p_rated = 0.6 # 额定功率 (kW）
    
    # #2.5MW 风机模拟参数
    # v_in = 3.0      # 切入风速 (m/s)
    # v_rated = 12.0  # 额定风速 (m/s
    # v_out = 25.0    # 切出风速 (m/s)
    # p_rated = 2500.0 # 额定功率 (kW

    # 风场模拟
    wind_field_manager = WindFieldManager(wind_speed_simulator=WindSpeedSimulator(tau=5.0, sigma=2.0, dt=1.0, mean_wind=10.0,tau_dir=30.0, sigma_dir=5.0, mean_dir=0.0))
    # wind_speeds 风速（秒）
    # wind_dirs 风向（秒）
    wind_speeds, wind_dirs = wind_field_manager.simulate(steps=1)

    # 求解1min均值风速，用于发布页面底部数据区域的有功功率（分钟）的计算
    points_per_min = int(60 / wind_field_manager.wind_speed_simulator.dt)
    num_mins = len(wind_speeds) // points_per_min
    wind_speeds_trimmed_min = wind_speeds[:num_mins * points_per_min]
    wind_speeds_min_average = wind_speeds_trimmed_min.reshape(num_mins, points_per_min).mean(axis=1)
    # 求解1h均值风速
    points_per_hour = int(3600 / wind_field_manager.wind_speed_simulator.dt)
    num_hours = len(wind_speeds) // points_per_hour
    # 只对完整小时计算平均值
    wind_speeds_trimmed_hour = wind_speeds[:num_hours * points_per_hour]
    wind_speeds_hour_average = wind_speeds_trimmed_hour.reshape(num_hours, points_per_hour).mean(axis=1)

    # 环境温度模拟
    # temperatures 环境温度（小时）
    temperature_simulator = TemperatureSimulator(tau=6.0, sigma=0.5, dt=1.0, mean_temp=20.0)
    temperatures = temperature_simulator.simulate(hours=24)

    # 风机功率和转速模拟
    # turbine_simulator = WindTurbinePowerSimulator(v_in=3.0, v_rated=12.0, v_out=25.0, p_rated=2500.0)
    turbine_simulator = WindTurbinePowerSimulator(v_in=2.0, v_rated=13.0, v_out=50.0, p_rated=0.6) #600W 风机
    # turbine_power_sec 有功功率 （秒）
    # turbine_rpm_sec 转速 (秒)
    wind_speeds = np.asarray([10])
    turbine_power_sec = turbine_simulator.power_from_speed(wind_speeds) #用于发布页面底部数据区域的有功功率（秒）
    turbine_rpm_sec = turbine_simulator.rpm_from_power(turbine_power_sec) #用于发布页面底部数据区域的转速（秒）

    # turbine_power_min 有功功率 （分钟）
    # turbine_rpm_min 转速 (分钟)
    turbine_power_min = turbine_simulator.power_from_speed(wind_speeds_min_average) #用于发布页面底部数据区域的有功功率（分钟）
    turbine_rpm_min = turbine_simulator.rpm_from_power(turbine_power_min)
    # turbine_power_hour 有功功率（小时）
    # turbine_rpm_hour 转速（小时）
    turbine_power_hour = turbine_simulator.power_from_speed(wind_speeds_hour_average) #用于发布页面右侧曲线功率的呈现
    turbine_rpm_hour = turbine_simulator.rpm_from_power(wind_speeds_hour_average)

    # 风机轴承温度模拟
    # bearing_temperatures 轴承温度（分钟）
    bearing_temp_simulator = BearingTemperatureSimulator(tau=10.0, sigma=1.0, dt=1.0, mean_temp=40.0)
    bearing_temperatures = bearing_temp_simulator.simulate(minutes=24*60)

    # 风机轴承振动模拟
    # bearing_vibrations 轴承振动（分钟）
    bearing_vibration_simulator = BearingVibrationSimulator()
    bearing_vibrations = bearing_vibration_simulator.simulate(steps=24*60)

    # 保存数据到csv
    save_csv(wind_speeds, wind_dirs, wind_speeds_min_average, turbine_power_min, turbine_rpm_min, bearing_temperatures, bearing_vibrations, wind_speeds_hour_average, turbine_power_hour, turbine_rpm_hour, temperatures, turbine_power_sec, turbine_rpm_sec)

    # 可视化结果
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 2, 1)
    # plt.plot(wind_speeds, label='Wind Speed (m/s)')
    # plt.title('Wind Speed Simulation')
    # plt.xlabel('Seconds')
    # plt.ylabel('Speed (m/s)')
    # plt.grid()
    # plt.legend()
    plt.plot(turbine_power_sec[-360:], label='Turbine Power (kW)', color='blue')
    plt.title('Turbine Power & RPM (Seconds Avg)')
    plt.xlabel('Seconds')
    plt.ylabel('Power (kW)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 2, 2)
    plt.plot(temperatures, label='Ambient Temperature (°C)', color='orange')
    plt.title('Ambient Temperature Simulation')
    plt.xlabel('Hours')
    plt.ylabel('Temperature (°C)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 2, 3)
    ax1 = plt.gca()
    line1, = ax1.plot(turbine_power_min, label='Turbine Power (kW)', color='green')
    ax1.set_xlabel('Minutes')
    ax1.set_ylabel('Power (kW)')
    ax1.grid(True)
    # 共享 X 轴的第二个 y 轴，用于 RPM
    ax2 = ax1.twinx()
    line2, = ax2.plot(turbine_rpm_min, label='Turbine RPM', color='tab:orange')
    ax2.set_ylabel('RPM')
    plt.title('Turbine Power & RPM (Minutes Avg)')
    # 合并两个轴的图例
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.subplot(3, 2, 4)
    ax1 = plt.gca()
    line1, = ax1.plot(turbine_power_hour, label='Turbine Power (kW)', color='green')
    ax1.set_xlabel('Hours')
    ax1.set_ylabel('Power (kW)')
    ax1.grid(True)
    # 共享 X 轴的第二个 y 轴，用于 RPM
    ax2 = ax1.twinx()
    line2, = ax2.plot(turbine_rpm_hour, label='Turbine RPM', color='tab:orange')
    ax2.set_ylabel('RPM')
    plt.title('Turbine Power & RPM (Hourly Avg)')
    # 合并两个轴的图例
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.subplot(3, 2, 5)
    plt.plot(bearing_temperatures, label='Bearing Temperature (°C)', color='red')
    plt.title('Bearing Temperature Simulation')
    plt.xlabel('Minutes')
    plt.ylabel('Temperature (°C)')
    plt.grid()
    plt.legend()

    plt.subplot(3, 2, 6)
    plt.plot(bearing_vibrations, label='Bearing Vibration (mm/s)', color='purple')
    plt.title('Bearing Vibration Simulation')
    plt.xlabel('Minutes')
    plt.ylabel('Vibration (mm/s)')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()