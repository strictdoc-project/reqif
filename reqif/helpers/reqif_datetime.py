import time
from datetime import datetime, timedelta, timezone


def create_reqif_datetime_now() -> str:
    """
    FIXME: Maybe there is an easier way of create this.
    """

    # Get the local time and UTC offset
    local_time = time.localtime()
    utc_offset = timedelta(
        seconds=-time.timezone if local_time.tm_isdst == 0 else -time.altzone
    )

    # Create a timezone object
    local_timezone = timezone(utc_offset)

    # Get the current time in the local timezone
    now = datetime.now(local_timezone)

    # Format the datetime in the ReqIF format
    formatted_time = reqif_datetime_format(now)

    return formatted_time


def reqif_datetime_format(datetime_obj: datetime) -> str:
    """
    Formats a date object to this format:
    2024-06-16T22:39:18.543+02:00
    FIXME: Maybe there is an easier way of create this.
    """

    formatted_time = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    formatted_time = (
        formatted_time[:23] + formatted_time[-5:-2] + ":" + formatted_time[-2:]
    )
    return formatted_time
