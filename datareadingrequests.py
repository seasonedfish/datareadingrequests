import json
import typing

import requests


class DataReading(typing.NamedTuple):
    """A data reading from a meter, with a quantity and a unit."""
    quantity: float
    unit: str


class UnsuccessfulRequest(Exception):
    """Raised when a request sent to the server is unsuccessful."""
    pass


class NoResponseList(UnsuccessfulRequest):
    """Raised when server returns no response list."""
    def __init__(self, bulk_request):
        super().__init__(
            f"The server returned no response list for {type(bulk_request)} bulk request"
        )


class NoDataReading(UnsuccessfulRequest):
    """Raised when server returns no data reading."""
    def __init__(self, facility, instance):
        super().__init__(
            f"The server returned no data reading for \"{facility}\" \"{instance}\""
        )


def get_value(facility, instance, live=True) -> DataReading:
    """
    Get the reading of a meter through Building Energy Gateway.

    Although mostly compatible with building_data_requests' function of the same name,
    note that if the server returns no data,
    datareadingrequests' version will raise an exception.

    :param facility: The facility in which the meter is located.
    :param instance: The meter's number.
    :param live: (optional) Whether to get a live reading.
        By default, the function will get a cached reading.
    :return: a DataReading namedtuple consisting of (quantity, unit).
    """
    args = {
        "facility": facility,
        "instance": instance,
    }
    if live:
        args[live] = True

    response = send_get_request(args)
    try:
        instance_response = response.json()["instance_response"]
    except TypeError:
        raise NoDataReading(facility, instance)
    if not instance_response["success"]:
        raise NoDataReading(facility, instance)

    data = instance_response["data"]
    return DataReading(data["presentValue"], data["units"])


def get_bulk(bulk_request: typing.Iterable[typing.Dict]) -> typing.Dict:
    """
    Get readings in bulk from Building Energy Gateway.

    Although mostly compatible with building_data_requests' function of the same name,
    note that if the server returns no data for any specific instance,
    datareadingrequests' version will raise an exception.

    :param bulk_request: An iterable, with each item specifying one instance.
        Each item should be a dictionary with keys "facility", "instance", and "label".
        "label" is optional.
    :return: A dictionary representing the server's JSON response.
        Inside this dictionary is ["rsp_list"], a list of the readings.
        ["rsp_list"] can be used to create a Pandas DataFrame.
    """
    response = send_get_request({"bulk": json.dumps(bulk_request)})
    try:
        response_dict = response.json()
    except json.JSONDecodeError:
        raise NoResponseList(bulk_request)

    if len(response_dict["rsp_list"]) == 0:
        raise NoResponseList(bulk_request)

    for r in response_dict["rsp_list"]:
        if not r["success"]:
            raise NoDataReading(r['facility'], r['instance'])

    return response_dict


def send_get_request(args):
    """
    Send an HTTP GET request to Building Energy Gateway.

    This is the datareadingrequests equivalent of
    building_data_requests' post_request().
    Note that it does not retry requests without SSL.

    :param args: Arguments for the request.
    :return: Response object.
    """
    return requests.get("https://energize.andoverma.us", params=args)
