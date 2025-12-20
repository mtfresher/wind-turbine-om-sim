import numpy as np
import matplotlib.pyplot as plt

def plot_turbine_power_and_rpm(power_data, rpm_data, time_data):
    """
    绘制风机功率和转速的可视化图表

    :param power_data: 风机功率数据（单位：kW）
    :param rpm_data: 风机转速数据（单位：rpm）
    :param time_data: 时间数据（单位：小时）
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制功率数据
    ax1.set_xlabel('时间 (小时)')
    ax1.set_ylabel('风机功率 (kW)', color='tab:blue')
    ax1.plot(time_data, power_data, color='tab:blue', label='功率')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid()

    # 创建第二个y轴用于绘制转速数据
    ax2 = ax1.twinx()
    ax2.set_ylabel('风机转速 (rpm)', color='tab:orange')
    ax2.plot(time_data, rpm_data, color='tab:orange', label='转速')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # 添加标题和图例
    plt.title('风机功率与转速可视化')
    fig.tight_layout()
    plt.show()