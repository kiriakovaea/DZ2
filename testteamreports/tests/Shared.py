import os
from json import JSONDecodeError

import datetime


def get_obj_from_json(response, obj_pattern):
    try:
        return obj_pattern.from_json(response.json())
    except JSONDecodeError:
        return None


def build_timestamp(value):
    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%dT%H:%M:%S"
    if type(value) == datetime.date:
        result = datetime.strftime(value, date_format)
        return result
    if type(value) == datetime:
        result = datetime.strftime(value, datetime_format)
        return result



