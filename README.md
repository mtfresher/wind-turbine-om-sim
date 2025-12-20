# wind-turbine-om-sim/wind-turbine-om-sim/README.md

# 风机运维模拟项目

该项目旨在模拟风机运维场景下的各种环境和设备参数，包括风场的风速和风向角模拟、环境温度的模拟、风机的功率和转速模拟，以及风机轴承的温度和振动模拟。

## 项目结构

```
wind-turbine-om-sim
├── src
│   ├── __init__.py                # 将src目录标记为一个Python包
│   ├── main.py                     # 应用程序入口点
│   ├── configs                     # 配置参数目录
│   │   ├── __init__.py
│   │   ├── wind_field_config.py    # 风场模拟配置
│   │   ├── temperature_config.py    # 温度模拟配置
│   │   ├── turbine_config.py       # 风机模拟配置
│   │   └── bearing_config.py       # 轴承模拟配置
│   ├── simulations                 # 模拟逻辑目录
│   │   ├── __init__.py
│   │   ├── wind                    # 风速和风向模拟
│   │   │   ├── __init__.py
│   │   │   ├── wind_speed_simu.py  # 风速模拟逻辑
│   │   │   └── wind_field_manager.py # 风场管理
│   │   ├── environment             # 环境模拟
│   │   │   ├── __init__.py
│   │   │   └── temperature_simulator.py # 温度模拟逻辑
│   │   ├── turbine                 # 风机模拟
│   │   │   ├── __init__.py
│   │   │   └── wind_turbine_power_simu.py # 风机功率和转速模拟
│   │   └── bearing                 # 轴承模拟
│   │       ├── __init__.py
│   │       ├── bearing_temp_simulator.py # 轴承温度模拟
│   │       └── bearing_vibration_simulator.py # 轴承振动模拟
│   ├── analysis                    # 数据分析目录
│   │   ├── __init__.py
│   │   ├── power_analysis.py       # 风机功率分析
│   │   ├── health_index.py         # 风机健康指数计算
│   │   └── anomaly_detection.py     # 风机异常检测
│   ├── visualization               # 可视化目录
│   │   ├── __init__.py
│   │   ├── plots_wind.py           # 风速和风向可视化
│   │   ├── plots_environment.py     # 环境温度可视化
│   │   ├── plots_turbine.py        # 风机功率和转速可视化
│   │   └── plots_bearing.py        # 轴承温度和振动可视化
│   └── types                       # 类型定义目录
│       └── index.py                # 项目类型和接口定义
├── tests                           # 测试目录
│   ├── __init__.py
│   ├── test_wind.py                # 风速和风向模拟测试
│   ├── test_temperature.py          # 温度模拟测试
│   ├── test_turbine.py             # 风机功率和转速测试
│   └── test_bearing.py             # 轴承模拟测试
├── requirements.txt                # 项目依赖包
├── pyproject.toml                  # 项目配置文件
└── README.md                       # 项目文档和使用说明
```

## 使用说明

1. **安装依赖**：请确保安装了项目所需的所有依赖包，可以通过以下命令安装：
   ```
   pip install -r requirements.txt
   ```

2. **运行模拟**：使用以下命令启动模拟：
   ```
   python src/main.py
   ```

3. **查看结果**：模拟结果将会在控制台输出，或根据具体实现保存到文件中。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证

该项目遵循MIT许可证。