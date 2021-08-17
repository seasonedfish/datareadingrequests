import json
import typing

import requests


class DataReading(typing.NamedTuple):
    """A data reading from a meter, with value and units."""
    value: float
    units: str


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
    return requests.get("https://energize.andoverma.us", params=args)
