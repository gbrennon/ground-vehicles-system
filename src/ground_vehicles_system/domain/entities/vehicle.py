from __future__ import annotations

from enum import StrEnum
import logging
import math
from uuid import uuid4

from ground_vehicles_system.domain.common.constants import GeodeticConstants
from ground_vehicles_system.domain.entities.base_entity import Entity
from ground_vehicles_system.domain.errors.vehicle_errors import (
    CannotChangeVelocityOfAccidentedVehicle,
    CrashedVehicleError
)
from ground_vehicles_system.domain.value_objects.velocity import (
    Velocity,
    VelocityConstants,
    VelocityUnit
)
from ground_vehicles_system.domain.value_objects.coordinates import Coordinates
from ground_vehicles_system.domain.value_objects.heading import Heading

_logger = logging.getLogger(__name__)


class VehicleState(StrEnum):
    """Enumeration for a vehicle's state."""
    STOPPED = "stopped"
    DRIVING = "driving"
    PARKING = "parking"
    ACCIDENTED = "accidented"


class Vehicle(Entity[str]):
    def __init__(
        self,
        vehicle_id: str,
        coordinates: Coordinates,
        velocity: Velocity,
        heading: Heading,
        state: VehicleState
    ) -> None:
        self._id = vehicle_id
        self._coordinates = coordinates
        self._velocity = velocity
        self._heading = heading
        self._state = state

    @classmethod
    def create(
        cls,
        coordinates: Coordinates,
        velocity: Velocity,
        vehicle_id: str | None = None,
        heading: Heading | None = None,
    ) -> Vehicle:
        """Factory method to create a Vehicle instance."""
        id = vehicle_id if vehicle_id is not None else uuid4().hex
        heading = heading if heading is not None else Heading(0.0)
        state = VehicleState.STOPPED if velocity.value == 0 else VehicleState.DRIVING

        return cls(id, coordinates, velocity, heading, state)

    @property
    def vehicle_id(self) -> str:
        return self._id

    @property
    def coordinates(self) -> Coordinates:
        return self._coordinates

    @property
    def velocity(self) -> Velocity:
        return self._velocity

    @property
    def heading(self) -> Heading:
        return self._heading

    def accelerate(self, amount: float, unit: VelocityUnit) -> None:
        """
        Accelerates the vehicle by the given amount.
        Returns a new Vehicle instance with the updated velocity and state.
        """
        if self._state == VehicleState.ACCIDENTED:
            _logger.info(
                f"Cannot accelerate: Vehicle {self._id} is in an accident."
            )
            raise CannotChangeVelocityOfAccidentedVehicle()

        delta = self._convert_velocity(amount, unit)
        new_mps = max(0.0, self._velocity.to_mps() + delta)
        self._velocity = Velocity(new_mps)

        old_state = self._state

        if  new_mps > 0:
            self._state = VehicleState.DRIVING
        else:
            if self._state == VehicleState.PARKING:
                self._state = VehicleState.PARKING
            else:
                self._state = VehicleState.STOPPED

        if old_state != self._state:
            _logger.info(f"Vehicle {self._id} is now {self._state.value}.")

    def decelerate(self, amount: float, unit: VelocityUnit) -> None:
        """
        Decelerates the vehicle by the given amount.
        Deceleration is simply a negative acceleration.
        Returns a new Vehicle instance with the updated velocity and state.
        """
        return self.accelerate(-amount, unit)

    def brake(self, amount: float, unit: VelocityUnit) -> None:
        """
        Brakes the vehicle by the given amount.
        This is an alias for the decelerate method, as braking is a form of deceleration.
        """
        return self.decelerate(amount, unit)

    def brake_to_a_stop(self) -> None:
        """
        Brakes the vehicle with maximum force to bring its velocity to 0.
        Returns a new Vehicle instance with velocity set to 0.
        """
        self.accelerate(-self._velocity.to_mps(), VelocityUnit.MPS)

    def turn(self, degrees: float) -> None:
        """
        Turns the vehicle by the given degrees.
        The heading is updated by adding the degrees to the current heading.
        Returns a new Vehicle instance with the updated heading.
        """
        if self._state == VehicleState.ACCIDENTED:
            _logger.info(f"Cannot turn: Vehicle {self._id} is in an accident.")
            raise CannotChangeVelocityOfAccidentedVehicle()

        self._heading = self._heading.turn(degrees)

        _logger.info(
            f"Vehicle {self._id} is now heading {self._heading.degrees:.2f} "
            "degrees."
        )

    def stop_engine(self) -> None:
        """
        Stops the vehicle's engine, setting its velocity to zero.
        Returns a new Vehicle instance with the updated velocity and state.
        """
        if self._state == VehicleState.ACCIDENTED:
            _logger.info(
                f"Vehicle {self._id} is already in an accident."
            )

        self._state = VehicleState.STOPPED
        self._velocity = Velocity(0.0)

    def move(
        self,
        time_delta_seconds: float,
        obstacle_found: bool,
        will_hit_obstacle: bool
    ) -> None:
        """
        Moves the vehicle based on its current velocity and heading.
        Returns a new Vehicle instance with the updated coordinates and state,
        or raises CrashedVehicleError if it hits an obstacle.
        """
        if self._state != VehicleState.DRIVING:
            return

        if obstacle_found:
            if will_hit_obstacle:
                _logger.error(
                    f"Vehicle {self._id} has crashed into an obstacle and is "
                    f"now in {VehicleState.ACCIDENTED.value} state."
                )
                self._state = VehicleState.ACCIDENTED
                raise CrashedVehicleError()
            else:
                _logger.warning(
                    f"Vehicle {self._id} detected an obstacle. "
                    "Stopping movement."
                )
                self.brake_to_a_stop()
                return

        velocity_mps = self.velocity.to_mps()

        # If the vehicle's velocity is 0, it shouldn't move
        if velocity_mps == 0.0:
            return

        delta_lat_per_second = (
            self._calculate_delta_lat(velocity_mps) * time_delta_seconds
        )
        delta_lon_per_second = (
            self._calculate_delta_lon(velocity_mps) * time_delta_seconds
        )

        self._coordinates = self._coordinates.move(
            delta_latitude=delta_lat_per_second,
            delta_longitude=delta_lon_per_second
        )

        distance_meters = velocity_mps * time_delta_seconds

        _logger.info(
            f"Vehicle {self._id} moved {distance_meters:.2f} meters to new "
            "position."
        )

    def _calculate_delta_lat(self, velocity_mps: float) -> float:
        return (
            velocity_mps * math.cos(self.heading.radians)
        ) / GeodeticConstants.METERS_PER_DEGREE_LATITUDE

    def _calculate_delta_lon(self, velocity_mps: float) -> float:
        return (
            velocity_mps * math.sin(self.heading.radians)
        ) / (
            GeodeticConstants.METERS_PER_DEGREE_LATITUDE * math.cos(
                math.radians(self.coordinates.latitude)
            )
        )

    def _convert_velocity(self, amount: float, unit: VelocityUnit) -> float:
        if unit == VelocityUnit.KPH:
            return amount * VelocityConstants.KILOMETERS_PER_HOUR_TO_METERS_PER_SECOND
        if unit == VelocityUnit.MPH:
            return amount * VelocityConstants.MILES_PER_HOUR_TO_METERS_PER_SECOND
        return amount

