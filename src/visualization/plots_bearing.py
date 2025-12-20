import numpy as np
import matplotlib.pyplot as plt

def plot_bearing_temperature(temperatures, time_hours):
    """
    绘制风机轴承温度变化图
    :param temperatures: 温度数据（numpy 数组）
    :param time_hours: 时间数据（numpy 数组）
    """
    plt.figure(figsize=(10, 4))
    plt.plot(time_hours, temperatures, label="Bearing Temperature", color='blue')
    plt.xlabel("Time (hours)")
    plt.ylabel("Temperature (°C)")
    plt.title("Bearing Temperature Over Time")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_bearing_vibration(vibrations, time_hours):
    """
    绘制风机轴承振动变化图
    :param vibrations: 振动数据（numpy 数组）
    :param time_hours: 时间数据（numpy 数组）
    """
    plt.figure(figsize=(10, 4))
    plt.plot(time_hours, vibrations, label="Bearing Vibration", color='red')
    plt.xlabel("Time (hours)")
    plt.ylabel("Vibration (mm/s)")
    plt.title("Bearing Vibration Over Time")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()