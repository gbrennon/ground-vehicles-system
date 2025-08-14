from ground_vehicles_system.domain.value_objects.heading import Heading


class TestHeading:
    def test_radians_when_value_is_zero_then_result_is_zero(self):

        actual_heading = Heading(0.0)

        expected = 0.0
        assert actual_heading.radians == expected

    def test_radians_when_value_is_90_then_result_is_pi_divided_by_2(self):
        actual_heading = Heading(90.0)

        expected = 1.5707963267948966  # π/2
        assert actual_heading.radians == expected

    def test_turn_when_0_but_turning_90_degrees_then_heading_is_90(self):
        actual_heading = Heading(0.0)
        delta_degrees = 90.0

        new_heading = actual_heading.turn(delta_degrees)

        expected = 90.0
        assert new_heading.degrees == expected

    def test_turn_when_0_but_turning_minus_90_degrees_then_heading_is_270(self):
        actual_heading = Heading(0.0)
        delta_degrees = -90.0

        new_heading = actual_heading.turn(delta_degrees)

        expected = 270.0
        assert new_heading.degrees == expected

    def test_turn_when_350_but_turning_20_degrees_then_heading_is_10(self):
        actual_heading = Heading(350.0)
        delta_degrees = 20.0

        new_heading = actual_heading.turn(delta_degrees)

        expected = 10.0
        assert new_heading.degrees == expected
