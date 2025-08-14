import pytest

from ground_vehicles_system.domain.value_objects.velocity import Velocity, VelocityUnit


class TestVelocity:
    def test_init_when_negative_value_then_negative_value(
        self
    ) -> None:
        actual_mps_value = -1.0

        velocity = Velocity(actual_mps_value)

        expected_value = -1.0
        assert velocity._value_mps == expected_value

    def test_init_when_value_is_zero_then_sets_value(self) -> None:
        actual_value = 0.0

        velocity = Velocity(actual_value)

        expected = 0.0
        assert velocity.to_mps() == expected

    def test_init_when_value_is_positive_then_sets_value(self) -> None:
        actual_value = 10.0

        velocity = Velocity(actual_value)

        expected = 10.0
        assert velocity.to_mps() == expected

    def test_from_unit_when_positive_value_and_unit_is_mps_then_sets_value(
        self
    ) -> None:
        actual_value = 10.0
        actual_unit = VelocityUnit.MPS

        velocity = Velocity.from_units(actual_value, actual_unit)

        expected = 10.0
        assert pytest.approx(velocity.to_mps()) == expected

    def test_from_unit_when_positive_value_and_unit_is_kph_then_sets_value(
        self
    ) -> None:
        actual_value = 36.0
        actual_unit = VelocityUnit.KPH

        velocity = Velocity.from_units(actual_value, actual_unit)

        expected = 10.0
        assert pytest.approx(velocity.to_mps()) == expected

    def test_from_unit_when_positive_value_and_unit_is_mph_then_sets_value(
        self
    ) -> None:
        actual_value = 22.36936
        actual_unit = VelocityUnit.MPH

        velocity = Velocity.from_units(actual_value, actual_unit)

        expected = 10.0
        assert pytest.approx(velocity.to_mps()) == expected

    def test_to_mps_when_value_is_set_in_mps_then_returns_same_value(self) -> None:
        actual_value = 10.0
        velocity = Velocity(actual_value)

        result = velocity.to_mps()

        expected = 10.0
        assert pytest.approx(result) == expected

    def test_to_kph_when_value_is_set_in_mps_then_converts_to_kph(self) -> None:
        actual_value = 10.0
        velocity = Velocity(actual_value)

        result = velocity.to_kph()

        expected = 36.0
        assert pytest.approx(result) == expected

    def test_to_mph_when_value_is_set_in_mps_then_converts_to_mph(self) -> None:
        actual_value = 10.0
        velocity = Velocity(actual_value)

        result = velocity.to_mph()

        expected = 22.36936
        assert pytest.approx(result) == expected

    def test_to_kph_when_value_is_set_in_kph_then_converts_to_kph(self) -> None:
        actual_value = 36.0
        velocity = Velocity.from_units(actual_value, VelocityUnit.KPH)

        result = velocity.to_kph()

        expected = 36.0
        assert pytest.approx(result) == expected

    def test_to_mph_when_value_is_set_in_kph_then_converts_to_mph(self) -> None:
        actual_value = 36.0
        velocity = Velocity.from_units(actual_value, VelocityUnit.KPH)

        result = velocity.to_mph()

        expected = 22.36936
        assert pytest.approx(result) == expected

    def test_to_kph_when_value_is_set_in_mph_then_converts_to_kph(self) -> None:
        actual_value = 22.36936
        velocity = Velocity.from_units(actual_value, VelocityUnit.MPH)

        result = velocity.to_kph()

        expected = 36.0
        assert pytest.approx(result) == expected

    def test_to_mph_when_value_is_set_in_mph_then_converts_to_mph(self) -> None:
        actual_value = 22.36936
        velocity = Velocity.from_units(actual_value, VelocityUnit.MPH)

        result = velocity.to_mph()

        expected = 22.36936
        assert result == expected

    def test_to_mps_when_value_is_set_in_kph_then_converts_to_mps(self) -> None:
        actual_value = 36.0
        velocity = Velocity.from_units(actual_value, VelocityUnit.KPH)

        result = velocity.to_mps()

        expected = 10.0
        assert pytest.approx(result) == expected

    def test_to_mps_when_value_is_set_in_mph_then_converts_to_mps(self) -> None:
        actual_value = 22.36936
        velocity = Velocity.from_units(actual_value, VelocityUnit.MPH)

        result = velocity.to_mps()

        expected = 10.0
        assert pytest.approx(result) == expected

    def test_immutability_when_trying_to_change_value_then_raises_error(self) -> None:
        actual_value = 10.0
        velocity = Velocity(actual_value)

        with pytest.raises(AttributeError):
            velocity._value_mps = 20.0 # type: ignore

    def test_immutability_when_trying_to_add_new_attribute_then_raises_error(
        self
    ) -> None:
        actual_value = 10.0
        velocity = Velocity(actual_value)

        with pytest.raises(AttributeError):
            velocity.new_attribute = "test" # type: ignore
