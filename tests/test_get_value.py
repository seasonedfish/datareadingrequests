import datareadingrequests as drr
import pytest


@pytest.mark.parametrize(
    "test_instance, expected_units",
    [("3007360", "kW"), (3007360, "kW")]
)
def test_proper_input(test_instance, expected_units):
    data_reading = drr.get_value("ahs", test_instance)
    assert isinstance(data_reading, drr.DataReading)
    assert isinstance(data_reading.value, float)
    assert data_reading.units == expected_units


def test_proper_input_legacy():
    value, units = drr.get_value("ahs", 3007360)
    assert isinstance(value, float)
    assert isinstance(units, str)


def test_improper_input():
    with pytest.raises(drr.NoDataReading):
        drr.get_value("ahs", -1)
    with pytest.raises(drr.NoDataReading):
        drr.get_value("", 3007360)
