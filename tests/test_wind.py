import numpy as np
import pytest
from src.simulations.wind.wind_speed_simu import WindSpeedSimulator

@pytest.fixture
def wind_speed_simulator():
    return WindSpeedSimulator(tau=5.0, sigma=2.0, dt=1.0, mean_wind=10.0)

def test_wind_speed_initialization(wind_speed_simulator):
    assert wind_speed_simulator.wind_speed == 10.0
    assert wind_speed_simulator.wind_dir == 0.0

def test_wind_speed_step(wind_speed_simulator):
    initial_speed = wind_speed_simulator.wind_speed
    wind_speed_simulator._step_speed()
    assert wind_speed_simulator.wind_speed != initial_speed

def test_wind_direction_step(wind_speed_simulator):
    initial_direction = wind_speed_simulator.wind_dir
    wind_speed_simulator._step_direction()
    assert wind_speed_simulator.wind_dir != initial_direction

def test_simulate_steps(wind_speed_simulator):
    steps = 10
    wind_speeds, wind_dirs = wind_speed_simulator.simulate(steps)
    assert len(wind_speeds) == steps
    assert len(wind_dirs) == steps
    assert all(isinstance(speed, float) for speed in wind_speeds)
    assert all(isinstance(direction, float) for direction in wind_dirs)