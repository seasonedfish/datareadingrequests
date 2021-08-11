import json
import typing

import requests


class DataReading(typing.NamedTuple):
    """A data reading from a meter, with value and units"""
    value: float
    units: str


class UnsuccessfulRequest(Exception):
    """Raised when server returns no data reading"""
    def __init__(self, facility, instance):
        super().__init__(
            f"The server returned no data reading for {facility} {instance}"
        )


def get_value(facility, instance, live=True) -> DataReading:
    args = {
        "facility": facility,
        "instance": instance,
    }
    if live:
        args[live] = True

    instance_response = send_get_request(args).json()["instance_response"]
    if not instance_response["success"]:
        raise UnsuccessfulRequest(facility, instance)

    data = instance_response["data"]
    return DataReading(data["presentValue"], data["units"])


def get_bulk(bulk_request):
    response_dict = send_get_request({"bulk": json.dumps(bulk_request)}).json()

    for r in response_dict["rsp_list"]:
        if r["success"] is False:
            raise UnsuccessfulRequest(r["facility"], r["instance"])

    return response_dict


def send_get_request(args):
    return requests.get("https://energize.andoverma.us", params=args)
