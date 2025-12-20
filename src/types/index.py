from typing import Protocol, Tuple

class WindSpeedSimulatorInterface(Protocol):
    def step(self) -> Tuple[float, float]:
        ...

    def simulate(self, steps: int) -> Tuple[list, list]:
        ...

class TemperatureSimulatorInterface(Protocol):
    def step(self, t_hour: float) -> float:
        ...

    def simulate(self, hours: int) -> list:
        ...

class WindTurbinePowerSimulatorInterface(Protocol):
    def power_from_speed(self, wind_speeds: list) -> list:
        ...

class BearingTemperatureSimulatorInterface(Protocol):
    def step(self) -> float:
        ...

    def simulate(self, hours: int) -> list:
        ...

class BearingVibrationSimulatorInterface(Protocol):
    def step(self) -> float:
        ...

    def simulate(self, hours: int) -> list:
        ...