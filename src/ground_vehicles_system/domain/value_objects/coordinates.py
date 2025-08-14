from __future__ import annotations

from dataclasses import dataclass

from ground_vehicles_system.domain.errors.coordinates_errors import (
    InvalidLatitudeError,
    InvalidLongitudeError,
)


@dataclass(frozen=True)
class Coordinates:
    """
    A Value Object representing a geographic position.
    The object is immutable and performs validation on creation.
    """
    latitude: float
    longitude: float

    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise InvalidLatitudeError()
        if not (-180 <= self.longitude <= 180):
            raise InvalidLongitudeError()

    def move(self, delta_latitude: float, delta_longitude: float) -> Coordinates:
        new_latitude = self.latitude + delta_latitude
        new_longitude = self.longitude + delta_longitude

        return Coordinates(new_latitude, new_longitude)
