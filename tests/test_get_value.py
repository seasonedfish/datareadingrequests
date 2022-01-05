import pytest

import datareadingrequests as drr

regular_arguments = [
    ("3007360", True, "kW"),
    (3007360, True, "kW"),
    ("3007360", False, "kW"),
    (3007360, False, "kW")
]


@pytest.mark.parametrize(
    "test_instance, test_is_live, expected_unit",
    regular_arguments
)
def test_proper_input_works(test_instance, test_is_live, expected_unit):
    data_reading = drr.get_value("ahs", test_instance, live=test_is_live)
    assert isinstance(data_reading, drr.DataReading)
    assert isinstance(data_reading.quantity, float)
    assert data_reading.unit == expected_unit


@pytest.mark.parametrize(
    "test_instance, test_is_live, expected_unit",
    regular_arguments
)
def test_proper_input_legacy_usage_works(test_instance, test_is_live, expected_unit):
    quantity, unit = drr.get_value("ahs", test_instance, live=test_is_live)
    assert isinstance(quantity, float)
    assert unit == expected_unit


@pytest.mark.parametrize(
    "test_facility, test_instance",
    [("ahs", -1), ("", 3007360)]
)
def test_improper_input_raises_exception(test_facility, test_instance):
    with pytest.raises(drr.NoDataReading):
        drr.get_value(test_facility, test_instance)
