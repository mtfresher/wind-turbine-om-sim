import numpy as np
import matplotlib.pyplot as plt

def plot_wind_data(wind_speeds, wind_dirs, time):
    """
    绘制风速和风向角的可视化图形。
    
    :param wind_speeds: 风速数据（列表或numpy数组）
    :param wind_dirs: 风向角数据（列表或numpy数组）
    :param time: 时间数据（列表或numpy数组）
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # 子图1：风速
    axes[0].plot(time, wind_speeds, label='Wind Speed (m/s)', color='blue')
    axes[0].set_ylabel('Wind Speed (m/s)')
    axes[0].set_title('Simulated Wind Speed')
    axes[0].grid()
    axes[0].legend()

    # 子图2：风向角
    axes[1].plot(time, wind_dirs, label='Wind Direction (degrees)', color='orange')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Wind Direction (degrees)')
    axes[1].set_title('Simulated Wind Direction')
    axes[1].grid()
    axes[1].legend()

    plt.tight_layout()
    plt.show()