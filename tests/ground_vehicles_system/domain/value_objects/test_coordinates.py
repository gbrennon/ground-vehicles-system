import pytest
from ground_vehicles_system.domain.errors.coordinates_errors import InvalidLatitudeError, InvalidLongitudeError
from ground_vehicles_system.domain.value_objects.coordinates import Coordinates


class TestCoordinates:
    def test_init_when_latitude_less_than_minimum_then_raises_invalid_latitude(self):
        actual_latitude = -91.0
        actual_longitude = 0.0

        with pytest.raises(InvalidLatitudeError):
            Coordinates(latitude=actual_latitude, longitude=actual_longitude)

    def test_init_when_latitude_more_than_maximum_then_raises_invalid_latitude(self):
        actual_latitude = 91.0
        actual_longitude = 0.0

        with pytest.raises(InvalidLatitudeError):
            Coordinates(latitude=actual_latitude, longitude=actual_longitude)

    def test_init_when_longitude_less_than_minimum_then_raises_invalid_longitude(self):
        actual_latitude = 0.0
        actual_longitude = -181.0

        with pytest.raises(InvalidLongitudeError):
            Coordinates(latitude=actual_latitude, longitude=actual_longitude)

    def test_init_when_longitude_more_than_maximum_then_raises_invalid_longitude(self):
        actual_latitude = 0.0
        actual_longitude = 181.0

        with pytest.raises(InvalidLongitudeError):
            Coordinates(latitude=actual_latitude, longitude=actual_longitude)

    def test_init_when_values_between_boundaries_then_set_them_to_attributes(self):
        actual_latitude = 34.0522
        actual_longitude = -118.2437

        coordinates = Coordinates(latitude=actual_latitude, longitude=actual_longitude)

        expected_latitude = 34.0522
        expected_longitude = -118.2437
        assert coordinates.latitude == expected_latitude
        assert coordinates.longitude == expected_longitude

    def test_move_when_deltas_are_positive_then_new_coordinates_are_correct(self):
        actual_coordinates = Coordinates(latitude=34.0522, longitude=-118.2437)
        delta_latitude = 0.1
        delta_longitude = 0.1

        new_coordinates = actual_coordinates.move(delta_latitude, delta_longitude)

        expected_latitude = 34.1522
        expected_longitude = -118.1437
        assert new_coordinates.latitude == expected_latitude
        assert pytest.approx(new_coordinates.longitude) == expected_longitude

    def test_move_when_deltas_are_negative_then_new_coordinates_are_correct(self):
        actual_coordinates = Coordinates(latitude=34.0522, longitude=-118.2437)
        delta_latitude = -0.1
        delta_longitude = -0.1

        new_coordinates = actual_coordinates.move(delta_latitude, delta_longitude)

        expected_latitude = 33.9522
        expected_longitude = -118.3437
        assert new_coordinates.latitude == expected_latitude
        assert pytest.approx(new_coordinates.longitude) == expected_longitude
