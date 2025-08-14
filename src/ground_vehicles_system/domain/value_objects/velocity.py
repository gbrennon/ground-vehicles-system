from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ground_vehicles_system.domain.errors.velocity_errors import (
    NotAllowedNegativeVelocityError
)


class VelocityConstants:
    """Constants for precise velocity conversions."""
    METERS_PER_SECOND_TO_KILOMETERS_PER_HOUR = 3600 / 1000  # 3.6
    METERS_PER_SECOND_TO_MILES_PER_HOUR = 3600 / 1609.344   # ~2.236936
    KILOMETERS_PER_HOUR_TO_METERS_PER_SECOND = (
        1 / METERS_PER_SECOND_TO_KILOMETERS_PER_HOUR

    )
    MILES_PER_HOUR_TO_METERS_PER_SECOND = 1 / METERS_PER_SECOND_TO_MILES_PER_HOUR
    KILOMETERS_PER_HOUR_TO_MILES_PER_HOUR = (
        METERS_PER_SECOND_TO_MILES_PER_HOUR * KILOMETERS_PER_HOUR_TO_METERS_PER_SECOND
    )
    MILES_PER_HOUR_TO_KILOMETERS_PER_HOUR = 1 / KILOMETERS_PER_HOUR_TO_MILES_PER_HOUR
class VelocityUnit(StrEnum):
    """Enumeration for standard velocity units."""
    MPS = "m/s"
    KPH = "km/h"
    MPH = "mph"


@dataclass(frozen=True)
class Velocity:
    """
    A Value Object representing velocity, normalized to meters per second.
    """
    _value_mps: float

    @classmethod
    def from_units(cls, value: float, unit: VelocityUnit) -> Velocity:
        if unit == VelocityUnit.KPH:
            value *= VelocityConstants.KILOMETERS_PER_HOUR_TO_METERS_PER_SECOND
        elif unit == VelocityUnit.MPH:
            value *= VelocityConstants.MILES_PER_HOUR_TO_METERS_PER_SECOND
        return cls(value)

    @property
    def value(self) -> float:
        return self._value_mps

    def to_mps(self) -> float:
        return self._value_mps

    def to_kph(self) -> float:
        return (
            self._value_mps * VelocityConstants.METERS_PER_SECOND_TO_KILOMETERS_PER_HOUR
        )

    def to_mph(self) -> float:
        return self._value_mps * VelocityConstants.METERS_PER_SECOND_TO_MILES_PER_HOUR
