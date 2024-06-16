import datetime
import re

from reqif.helpers.reqif_datetime import (
    create_reqif_datetime_now,
    reqif_datetime_format,
)

PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"


def test_reqif_datetime_format_tz_plus() -> None:
    date = datetime.datetime(2018, 6, 6, 23, 59, 59, 999000)

    utc_plus_2 = datetime.timezone(datetime.timedelta(hours=2))
    date = date.replace(tzinfo=utc_plus_2)

    reqif_datetime = reqif_datetime_format(date)
    assert reqif_datetime == "2018-06-06T23:59:59.999+02:00"
    assert re.match(PATTERN, reqif_datetime)


def test_reqif_datetime_format_tz_minus() -> None:
    date = datetime.datetime(2018, 6, 6, 23, 59, 59, 999000)

    utc_minus_2 = datetime.timezone(datetime.timedelta(hours=-2))
    date = date.replace(tzinfo=utc_minus_2)

    reqif_datetime = reqif_datetime_format(date)
    assert reqif_datetime == "2018-06-06T23:59:59.999-02:00"
    assert re.match(PATTERN, reqif_datetime)


def test_create_reqif_datetime_now() -> None:
    date = create_reqif_datetime_now()
    assert re.match(PATTERN, date)
