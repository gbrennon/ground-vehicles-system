import pytest

from ground_vehicles_system.domain.entities.vehicle import Vehicle, VehicleState
from ground_vehicles_system.domain.errors.vehicle_errors import (
    CannotChangeVelocityOfAccidentedVehicle,
    CrashedVehicleError
)
from ground_vehicles_system.domain.value_objects.coordinates import Coordinates
from ground_vehicles_system.domain.value_objects.heading import Heading
from ground_vehicles_system.domain.value_objects.velocity import Velocity, VelocityUnit


class TestVehicle:
    @pytest.fixture
    def coordinates(self) -> Coordinates:
        return Coordinates(34.0522, -118.2437)

    @pytest.fixture
    def velocity(self) -> Velocity:
        return Velocity(10.0)

    def test_init_when_heading_then_use_provided_heading(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        heading = Heading(50)

        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=heading,
            state=VehicleState.STOPPED
        )

        assert vehicle._heading == heading

    def test_create_when_vehicle_id_is_none_then_generate_id(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle_id = None

        vehicle = Vehicle.create(
            vehicle_id=vehicle_id,
            coordinates=coordinates,
            velocity=velocity,
        )

        assert vehicle._id is not None

    def test_create_when_no_vehicle_id_then_generate_id(
        self
    ) -> None:
        actual_coordinates = Coordinates(34.0522, -118.2437)
        actual_velocity = Velocity(10.0)

        vehicle = Vehicle.create(
            coordinates=actual_coordinates,
            velocity=actual_velocity,
        )

        assert vehicle._id is not None

    def test_create_when_vehicle_id_then_use_provided_id(
        self,
        coordinates: Coordinates,
        velocity: Velocity,
    ) -> None:
        vehicle_id = "vehicle_123"

        vehicle = Vehicle.create(
            coordinates=coordinates,
            velocity=velocity,
            vehicle_id=vehicle_id,
        )

        assert vehicle._id == vehicle_id

    def test_create_when_heading_then_use_provided_heading(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        heading = Heading(50)

        vehicle = Vehicle.create(
            coordinates=coordinates,
            velocity=velocity,
            heading=heading,
        )

        assert vehicle._heading == heading

    def test_create_when_no_heading_then_default_heading(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle.create(
            coordinates=coordinates,
            velocity=velocity,
        )

        expected_heading = Heading(0.0)
        assert vehicle._heading == expected_heading

    def test_vehicle_id_property(
        self, coordinates: Coordinates, velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_123",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(0.0),
            state=VehicleState.STOPPED
        )

        expected_vehicle_id = "vehicle_123"
        assert vehicle.vehicle_id == expected_vehicle_id

    def test_coordinates_property(
        self, coordinates: Coordinates, velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_123",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(0.0),
            state=VehicleState.STOPPED
        )

        coordinates = vehicle.coordinates

        expected_coordinates = coordinates
        assert coordinates == expected_coordinates

    def test_velocity_property(
        self, coordinates: Coordinates, velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_123",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(0.0),
            state=VehicleState.STOPPED
        )

        velocity = vehicle.velocity

        expected_velocity = velocity
        assert vehicle.velocity == expected_velocity

    def test_heading_property(
        self, coordinates: Coordinates, velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_123",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(0.0),
            state=VehicleState.STOPPED
        )

        heading = vehicle.heading

        expected_heading = Heading(0.0)
        assert heading == expected_heading

    def test_accelerate_when_accidented_then_raises_exception(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        with pytest.raises(CannotChangeVelocityOfAccidentedVehicle):
            vehicle.accelerate(5.0, VelocityUnit.MPS)

    def test_accelerate_when_new_mps_bigger_then_zero_then_state_driving(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.DRIVING

    def test_accelerate_when_new_mps_zero_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.accelerate(-5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_accelerate_when_negative_new_mps_and_vehicle_is_parking_then_state_parking(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.accelerate(-5.0, VelocityUnit.MPS)

        expected_state = VehicleState.PARKING
        assert vehicle._state == expected_state

    def test_accelerate_when_negative_amount_then_velocity_zero(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.accelerate(-5.0, VelocityUnit.MPS)

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_accelerate_when_positive_amount_then_velocity_increases(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        expected_velocity = Velocity(5.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_accelerate_when_velocity_is_zero_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.DRIVING

    def test_accelerate_when_positive_velocity_then_state_driving(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.DRIVING

    def test_accelerate_when_negative_velocity_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(-10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_accelerate_when_negative_velocity_and_amount_is_negative_then_stat_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(-10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.accelerate(-5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_accelerate_when_negative_velocity_and_amount_is_positiv_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(-10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_accelerate_when_negative_velocity_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(-10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.accelerate(0.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_accelerate_when_negative_velocity_and_state_is_parking_then_state_parking(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(-10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.accelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.PARKING

    def test_decelerate_when_accidented_then_raises_exception(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        with pytest.raises(CannotChangeVelocityOfAccidentedVehicle):
            vehicle.decelerate(5.0, VelocityUnit.MPS)

    def test_decelerate_when_positive_new_mps_then_state_driving(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.decelerate(5.0, VelocityUnit.MPS)

        expected_state = VehicleState.DRIVING
        assert vehicle._state == expected_state

    def test_decelerate_when_new_mps_is_zero_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.decelerate(10.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_decelerate_when_positive_amount_and_vehicle_is_parking_then_state_parking(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.decelerate(5.0, VelocityUnit.MPS)

        expected_state = VehicleState.DRIVING
        assert vehicle._state == expected_state

    def test_decelerate_when_negative_amount_then_velocity_zero(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.decelerate(15.0, VelocityUnit.MPS)

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_decelerate_when_positive_amount_then_velocity_decreases(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.decelerate(5.0, VelocityUnit.MPS)

        expected_velocity = Velocity(5.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_decelerate_when_velocity_is_zero_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.decelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_decelerate_when_positive_velocity_then_state_driving(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.decelerate(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.DRIVING

    def test_brake_when_accidented_then_raises_exception(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        with pytest.raises(CannotChangeVelocityOfAccidentedVehicle):
            vehicle.brake(10, VelocityUnit.MPS)

    def test_brake_when_new_mps_bigger_then_zero_then_state_driving(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(20.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.brake(10, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.DRIVING

    def test_brake_when_new_mps_zero_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.brake(10, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_brake_when_negative_new_mps_and_vehicle_is_parking_then_state_parking(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.brake(5.0, VelocityUnit.MPS)

        expected_state = VehicleState.PARKING
        assert vehicle._state == expected_state

    def test_brake_when_negative_new_mps_then_velocity_zero(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.brake(5.0, VelocityUnit.MPS)

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_brake_when_positive_amount_then_velocity_decreases(
        self,
        coordinates: Coordinates,
    ) -> None:
        initial_velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=initial_velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.brake(5.0, VelocityUnit.MPS)

        assert vehicle._velocity.value < initial_velocity.value

    def test_brake_when_velocity_is_zero_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.brake(5.0, VelocityUnit.MPS)

        assert vehicle._state == VehicleState.STOPPED

    def test_brake_to_a_stop_when_state_is_parking_then_state_parking(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.brake_to_a_stop()

        assert vehicle._state == VehicleState.PARKING

    def test_brake_to_a_stop_when_state_is_driving_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(10.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.brake_to_a_stop()

        assert vehicle._state == VehicleState.STOPPED

    def test_brake_to_a_stop_when_state_is_stopped_then_state_stopped(
        self,
        coordinates: Coordinates,
    ) -> None:
        velocity = Velocity(0.0)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.brake_to_a_stop()

        assert vehicle._state == VehicleState.STOPPED

    def test_brake_to_a_stop_when_state_is_accidented_then_raise_exception(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        with pytest.raises(CannotChangeVelocityOfAccidentedVehicle):
            vehicle.brake_to_a_stop()

    def test_turn_when_accidented_then_raises_exception(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        with pytest.raises(CannotChangeVelocityOfAccidentedVehicle):
            vehicle.turn(45.0)

    def test_turn_when_positive_degrees_then_heading_changes(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(45.0)

        expected_heading = Heading(135.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_negative_degrees_then_heading_changes(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(-45.0)

        expected_heading = Heading(45.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_zero_degrees_then_heading_remains_same(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(0.0)

        expected_heading = Heading(90.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_360_then_heading_is_zero(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(360.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(0.0)

        expected_heading = Heading(0.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_0_and_turning_90_degrees_then_heading_is_90(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(0.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(90.0)

        expected_heading = Heading(90.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_0_and_turning_minus_90_degrees_then_heading_is_270(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(0.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(-90.0)

        expected_heading = Heading(270.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_350_and_turning_20_degrees_then_heading_is_10(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(350.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(20.0)

        expected_heading = Heading(10.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_10_and_turning_minus_20_degrees_then_heading_is_350(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(10.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(-20.0)

        expected_heading = Heading(350.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_180_and_turning_90_degrees_then_heading_is_270(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(180.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(90.0)

        expected_heading = Heading(270.0)
        assert vehicle._heading == expected_heading

    def test_turn_when_heading_is_180_and_turning_minus_90_degrees_then_heading_is_90(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(180.0),
            state=VehicleState.DRIVING
        )

        vehicle.turn(-90.0)

        expected_heading = Heading(90.0)
        assert vehicle._heading == expected_heading

    def test_stop_engine_when_accidented_then_state_changes_to_stopped(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        vehicle.stop_engine()

        expected_state = VehicleState.STOPPED
        assert vehicle._state == expected_state

    def test_stop_engine_when_driving_then_state_changes_to_stopped(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.stop_engine()

        expected_state = VehicleState.STOPPED
        assert vehicle._state == expected_state

    def test_stop_engine_when_parking_then_state_changes_to_stopped(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.stop_engine()

        expected_state = VehicleState.STOPPED
        assert vehicle._state == expected_state

    def test_stop_engine_when_stopped_then_state_remains_stopped(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.stop_engine()

        expected_state = VehicleState.STOPPED
        assert vehicle._state == expected_state

    def test_stop_engine_when_state_is_accidented_then_velocity_zero(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        vehicle.stop_engine()

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_stop_engine_when_state_is_driving_then_velocity_zero(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.stop_engine()

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_stop_engine_when_state_is_parking_then_velocity_zero(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.PARKING
        )

        vehicle.stop_engine()

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_stop_engine_when_state_is_stopped_then_velocity_zero(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.stop_engine()

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_stop_engine_when_state_is_accidented_then_velocity_is_zero(
        self,
        coordinates: Coordinates,
        velocity: Velocity
    ) -> None:
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.ACCIDENTED
        )

        vehicle.stop_engine()

        expected_velocity = Velocity(0.0)
        assert vehicle._velocity.value == expected_velocity.value

    def test_move_when_not_driving_then_coordinate_still_the_same(
        self,
        velocity: Velocity
    ) -> None:
        coordinates = Coordinates(34.0522, -118.2437)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.STOPPED
        )

        vehicle.move(10.0, False, False)

        expected_coordinates = Coordinates(34.0522, -118.2437)
        assert vehicle._coordinates == expected_coordinates

    def test_move_when_driving_and_not_obstacle_then_coordinates_change(
        self,
        velocity: Velocity
    ) -> None:
        coordinates = Coordinates(34.0522, -118.2437)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.move(10.0, False, False)

        assert vehicle._coordinates != coordinates

    def test_move_when_obstacle_and_hit_obstacle_then_crashed_vehicle_error(
        self,
        velocity: Velocity
    ) -> None:
        coordinates = Coordinates(34.0522, -118.2437)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        with pytest.raises(CrashedVehicleError):
            vehicle.move(10.0, True, True)

    def test_move_when_obstacle_and_not_hit_obstacle_then_brake_to_a_stop(
        self,
        velocity: Velocity
    ) -> None:
        coordinates = Coordinates(34.0522, -118.2437)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.move(10.0, True, False)

        expected_state = VehicleState.STOPPED
        assert vehicle._state == expected_state

    def test_move_when_velocity_mps_is_zero_then_coordinates_still_the_same(
        self,
        velocity = Velocity(0.0)
    ) -> None:
        coordinates = Coordinates(34.0522, -118.2437)
        vehicle = Vehicle(
            vehicle_id="vehicle_1",
            coordinates=coordinates,
            velocity=velocity,
            heading=Heading(90.0),
            state=VehicleState.DRIVING
        )

        vehicle.move(10.0, False, False)

        expected_coordinates = Coordinates(34.0522, -118.2437)
        assert vehicle._coordinates == expected_coordinates
