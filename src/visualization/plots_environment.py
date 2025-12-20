import numpy as np
import matplotlib.pyplot as plt

def plot_temperature(temperatures: np.ndarray, time_hours: np.ndarray):
    """
    绘制环境温度变化图
    :param temperatures: 温度时间序列（numpy 数组）
    :param time_hours: 时间序列（numpy 数组，单位：小时）
    """
    plt.figure(figsize=(10, 4))
    plt.plot(time_hours, temperatures, label="Temperature", color='blue')
    plt.xlabel("Time (hour)")
    plt.ylabel("Temperature (°C)")
    plt.title("Simulated Ambient Temperature Over Time")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_temperature_with_noise(temperatures: np.ndarray, time_hours: np.ndarray, noise: np.ndarray):
    """
    绘制带噪声的环境温度变化图
    :param temperatures: 温度时间序列（numpy 数组）
    :param time_hours: 时间序列（numpy 数组，单位：小时）
    :param noise: 温度噪声（numpy 数组）
    """
    plt.figure(figsize=(10, 4))
    plt.plot(time_hours, temperatures, label="Temperature", color='blue')
    plt.plot(time_hours, temperatures + noise, label="Temperature with Noise", color='red', alpha=0.5)
    plt.xlabel("Time (hour)")
    plt.ylabel("Temperature (°C)")
    plt.title("Simulated Ambient Temperature with Noise")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()