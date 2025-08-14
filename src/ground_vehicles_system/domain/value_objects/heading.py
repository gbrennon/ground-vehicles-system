from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Heading:
    degrees: float

    @property
    def radians(self) -> float:
        return math.radians(self.degrees)

    def turn(self, delta_degrees: float) -> Heading:
        new_heading = (self.degrees + delta_degrees) % 360
        return Heading(new_heading)
