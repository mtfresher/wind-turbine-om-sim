import numpy as np
import pytest
from src.simulations.environment.temperature_simulator import TemperatureSimulator

@pytest.fixture
def temperature_simulator():
    tau = 6.0
    sigma = 0.5
    dt = 1.0
    mean_temp = 20.0
    daily_amp = 5.0
    daily_phase = -9.0
    return TemperatureSimulator(tau, sigma, dt, mean_temp, daily_amp, daily_phase)

def test_initial_temperature(temperature_simulator):
    assert temperature_simulator.current_temp == temperature_simulator.mean_temp

def test_temperature_step(temperature_simulator):
    initial_temp = temperature_simulator.current_temp
    temperature_simulator.step(0)
    assert temperature_simulator.current_temp != initial_temp

def test_temperature_simulation_length(temperature_simulator):
    hours = 72
    temperatures = temperature_simulator.simulate(hours)
    assert len(temperatures) == hours

def test_daily_cycle(temperature_simulator):
    temp_at_noon = temperature_simulator.step(12)
    temp_at_midnight = temperature_simulator.step(0)
    assert temp_at_noon > temp_at_midnight  # Expecting higher temperature at noon than midnight