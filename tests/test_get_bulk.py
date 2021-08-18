import pytest

import datareadingrequests as drr


def test_proper_input_works():
    bulk_request = [
        {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
        {"facility": "ahs", "instance": "3001477", "label": "AHS 351 CO2"}
    ]
    bulk_response = drr.get_bulk(bulk_request)
    assert all(
        isinstance(specific_response["presentValue"], float)
        for specific_response in bulk_response["rsp_list"]
    )


def test_non_iterable_input_raises_exception():
    with pytest.raises(drr.NoResponseList):
        drr.get_bulk(0)


def test_empty_iterable_input_raises_exception():
    bulk_request = []
    with pytest.raises(drr.NoResponseList):
        drr.get_bulk(bulk_request)


@pytest.mark.parametrize(
    "bulk_request",
    [
        [
            {"facility": "ahs", "instance": "", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
            {"facility": "ahs", "instance": "", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "", "instance": "3001477", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
            {"facility": "", "instance": "3001477", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "", "instance": "", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
            {"facility": "", "instance": "", "label": "AHS 351 CO2"}
        ]
    ]
)
def test_empty_parameter_raises_exception(bulk_request):
    with pytest.raises(drr.NoDataReading):
        drr.get_bulk(bulk_request)


@pytest.mark.parametrize(
    "bulk_request",
    [
        [
            {"facility": "ahs", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
            {"facility": "ahs", "label": "AHS 351 CO2"}
        ],
        [
            {"instance": "3001477", "label": "AHS 351 CO2"}
        ],
        [
            {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
            {"instance": "3001477", "label": "AHS 351 CO2"}
        ],
        [
            {"label": "AHS 351 CO2"}
        ],
        [
            {"facility": "ahs", "instance": "3001489", "label": "AHS 351 Temperature"},
            {"label": "AHS 351 CO2"}
        ]
    ]
)
def test_missing_parameter_raises_exception(bulk_request):
    with pytest.raises(drr.NoDataReading):
        drr.get_bulk(bulk_request)


@pytest.mark.parametrize(
    "bulk_request",
    [
        [
            {"facility": "ahs", "instance": -1, "label": "AHS 351 Temperature"}
        ],
        [
            {"facility": -1, "instance": "3001489", "label": "AHS 351 Temperature"},
        ]
    ]
)
def test_improper_parameter_raises_exception(bulk_request):
    with pytest.raises(drr.NoDataReading):
        drr.get_bulk(bulk_request)
