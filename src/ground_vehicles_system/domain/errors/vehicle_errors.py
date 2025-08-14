class CannotChangeVelocityOfAccidentedVehicle(ValueError):
    """Raised when trying to set a velocity for an accidented vehicle."""
    def __init__(self) -> None:
        self._message = "Cannot set a velocity for an accidented vehicle."
        super().__init__(self._message)

class CrashedVehicleError(ValueError):
    """Raised when a vehicle is in an accident state."""
    def __init__(self) -> None:
        self._message = "Vehicle is in an accident state."
        super().__init__(self._message)
