import pytest

import datareadingrequests as drr


@pytest.mark.parametrize(
    "test_instance, expected_units",
    [("3007360", "kW"), (3007360, "kW")]
)
def test_proper_input_works(test_instance, expected_units):
    data_reading = drr.get_value("ahs", test_instance)
    assert isinstance(data_reading, drr.DataReading)
    assert isinstance(data_reading.value, float)
    assert data_reading.units == expected_units


@pytest.mark.parametrize(
    "test_instance, expected_units",
    [("3007360", "kW"), (3007360, "kW")]
)
def test_proper_input_legacy_usage_works(test_instance, expected_units):
    value, units = drr.get_value("ahs", test_instance)
    assert isinstance(value, float)
    assert units == expected_units


@pytest.mark.parametrize(
    "test_instance, test_instance",
    [("ahs", -1), ("", 3007360)]
)
def test_improper_input_raises_exception(test_facility, test_instance):
    with pytest.raises(drr.NoDataReading):
        drr.get_value(test_facility, test_instance)
