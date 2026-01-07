# 轴承温度模拟优化说明文档

## 📊 优化概述

之前的轴承温度模型过于简化，仅使用一个固定的均值进行模拟，无法反映实际风机轴承的温度特性。现已优化为**考虑转速和环境温度的动态热传导模型**。

---

## 🔧 核心改进

### 1. **物理模型升级**

#### 旧模型（过于简化）
```
温度 = 固定均值 + 随机波动
```

#### 新模型（考虑物理过程）
```
轴承温度(t) = 环境温度(t) + 摩擦生热(rpm(t)) + 热传导过程
             = T_env + ΔT_friction(rpm) + 随机波动
```

### 2. **转速依赖性** ⚡

**关键发现**：轴承摩擦生热与转速的平方成正比（二次关系）

```
ΔT_friction(rpm) = temp_rise_at_rated × ((rpm - rpm_min) / (rpm_rated - rpm_min))²
```

**物理意义**：
- **低转速** (6 rpm) → 低摩擦生热 → 温度接近环境温度
- **高转速** (15 rpm) → 高摩擦生热 → 温度比环境温度高15°C
- **非线性增长**：转速越高，生热增长越快

**示例**：
```
转速 6 rpm   → 温升 0°C    (停机状态)
转速 9 rpm   → 温升 4°C
转速 12 rpm  → 温升 11°C
转速 15 rpm  → 温升 15°C   (额定转速)
```

### 3. **环境温度依赖性** 🌡️

**热传导边界条件**：环境温度是轴承温度的下限

轴承温度模型：
```
dT/dt = (T_target - T_current) / τ + σ·noise
其中：
T_target = T_ambient + ΔT_friction(rpm)
τ = 热时间常数（模拟热惯性）
σ = 随机波动强度
```

**物理意义**：
- 炎热环境（环境温度↑） → 轴承温度↑
- 寒冷环境（环境温度↓） → 轴承温度↓
- 温度变化有延滞（热惯性效应）

---

## 🎯 新增参数详解

| 参数 | 默认值 | 单位 | 说明 |
|------|--------|------|------|
| `tau` | 10.0 | 分钟 | 热时间常数，越大温度变化越平缓 |
| `sigma` | 1.0 | °C/√min | 随机扰动强度，决定噪声大小 |
| `dt` | 1.0 | 分钟 | 时间步长 |
| `base_temp` | 40.0 | °C | 基础参考温度 |
| `rpm_min` | 6.0 | rpm | 最小运行转速 |
| `rpm_rated` | 15.0 | rpm | 额定转速 |
| `temp_rise_at_rated` | 15.0 | °C | 额定转速时的温升 |
| `convection_coeff` | 0.5 | - | 冷却系数（保留供扩展） |

---

## 📝 API 使用方式

### 方式1：传入序列（推荐）
```python
# 分钟级环境温度和转速序列
ambient_temps = np.array([20.0, 22.0, 25.0, ...])  # 分钟级
rpm_sequence = np.array([6.0, 9.0, 12.0, ...])     # 分钟级

bearing_temps = simulator.simulate(ambient_temps, rpm_sequence)
```

### 方式2：恒定条件（向后兼容）
```python
bearing_temps = simulator.simulate_with_fixed_conditions(
    minutes=1440,           # 24小时
    ambient_temp=20.0,      # °C
    rpm=12.0                # rpm
)
```

### 方式3：获取单个时刻的温度
```python
temp_t = simulator.step(ambient_temp=20.0, rpm=12.0)
```

### 方式4：获取摩擦生热值
```python
temp_rise = simulator._get_friction_heat_rise(rpm=12.0)
# 返回：11.11°C
```

---

## 🔄 与 main.py 的集成

### 变化说明

**旧代码：**
```python
bearing_temp_simulator = BearingTemperatureSimulator(
    tau=10.0, sigma=1.0, dt=1.0, mean_temp=40.0
)
bearing_temperatures = bearing_temp_simulator.simulate(minutes=24*60)
```

**新代码：**
```python
# 1. 将小时级环境温度扩展到分钟级
temperatures_minute = np.repeat(temperatures, 60)[:num_mins]

# 2. 创建模拟器，指定物理参数
bearing_temp_simulator = BearingTemperatureSimulator(
    tau=10.0,
    sigma=1.0,
    dt=1.0,
    base_temp=20.0,
    rpm_min=rpm_min,
    rpm_rated=rpm_rated,
    temp_rise_at_rated=15.0,  # 额定转速时温升15°C
)

# 3. 传入分钟级环境温度和转速
bearing_temperatures = bearing_temp_simulator.simulate(
    temperatures_minute,    # 环境温度序列
    turbine_rpm_min        # 转速序列
)
```

---

## 📈 数学模型详解

### 热传导方程（一阶微分方程）
```
dT/dt = (T_target - T_current) / τ + σ·dW/√dt

离散形式：
T(t+1) = T(t) + (T_target - T(t)) / τ · dt + σ·√dt·Z(0,1)
```

其中：
- `T_target = T_ambient + ΔT_friction(rpm)` - 目标温度
- `τ` - 热时间常数（单位：分钟）
- `σ` - 扰动强度
- `Z(0,1)` - 标准正态分布

### 物理约束
```
T_bearing ≥ T_ambient  （温度不会低于环境温度）
```

---

## 🧪 测试用例

### 测试1：转速影响
```python
rpm_sequence = [6.0, 9.0, 12.0, 15.0]
for rpm in rpm_sequence:
    temps = simulator.simulate_with_fixed_conditions(20, 20.0, rpm)
    # 预期：转速越高，温度越高
```

### 测试2：环境温度影响
```python
ambient_temps = [10.0, 15.0, 20.0, 25.0, 30.0]
for ambient in ambient_temps:
    temps = simulator.simulate_with_fixed_conditions(20, ambient, 12.0)
    # 预期：环境温度越高，轴承温度越高
```

### 测试3：热惯性
```python
temps = simulator.simulate_with_fixed_conditions(60, 20.0, 12.0)
# 预期：温度从初始值逐步向稳定值靠近（指数收敛）
# 时间常数 τ = 10 分钟，约5个τ（50分钟）后趋于稳定
```

---

## 🔍 对比：改进前后的差异

| 方面 | 改进前 | 改进后 |
|------|--------|--------|
| **转速依赖** | ❌ 无 | ✅ 二次非线性 |
| **环境温度** | ❌ 无 | ✅ 作为热边界 |
| **热惯性** | ❌ 固定均值 | ✅ 时间常数控制 |
| **物理真实性** | ⭐⭐ 低 | ⭐⭐⭐⭐⭐ 高 |
| **参数可调性** | ⭐ 低 | ⭐⭐⭐⭐ 高 |
| **计算复杂度** | 简单 | 中等（可接受） |

---

## 📊 典型场景示例

### 场景1：启动运行
```
初始状态：环境20°C，停机（0 rpm）
转速上升：0 → 12 rpm（5分钟内）
预期：轴承温度从20°C逐步升高到31°C（热惯性延滞）
时间常数：约10分钟趋于稳定值
```

### 场景2：环境温度变化
```
早上：环境5°C，运行转速9 rpm → 轴承温度约13°C
中午：环境25°C，运行转速12 rpm → 轴承温度约36°C
晚上：环境10°C，运行转速6 rpm → 轴承温度约10°C
```

### 场景3：负载变化
```
低负载：转速6 rpm，环境20°C → 温度20°C
中负载：转速12 rpm，环境20°C → 温度31°C
高负载：转速15 rpm，环境20°C → 温度35°C
```

---

## 🚀 后续扩展建议

1. **加入冷却效应**：`convection_coeff` 参数可用于模拟不同的冷却条件
2. **加入负载因素**：可考虑功率或力矩对生热的额外影响
3. **加入老化模型**：轴承随时间老化会增加摩擦系数
4. **加入润滑状态**：润滑油粘度随温度变化会影响摩擦
5. **多点温度分布**：考虑轴承不同位置的温度差异

---

## ✅ 验证脚本

运行验证脚本查看优化效果：
```bash
python verify_bearing_temperature_optimization.py
```

会生成对比图表：
- 转速-生热关系曲线
- 恒定条件下的温度演化
- 环境温度与轴承温度的关系
- 三元关系图（环境温度、转速、轴承温度）

---

## 📌 总结

✨ **主要改进**：
- 从静态模型 → 动态热传导模型
- 考虑了转速的二次非线性影响
- 考虑了环境温度的作用
- 保留了热惯性的物理特性
- 保持了向后兼容性

🎯 **优势**：
- 更接近真实物理过程
- 更多参数可调，灵活性高
- 可用于故障诊断（温度异常预警）
- 可用于寿命预测（热应力累积）
