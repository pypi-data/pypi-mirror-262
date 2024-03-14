import re
import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional


# Function to get the time today in the YYYY-MM-DD format.
def get_time_today() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


# Function to get the time 3 years ago in the YYYY-MM-DD format.
def get_time_1_years_ago() -> str:
    return (datetime.datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")


def get_default_date_range() -> str:
    return "({0}, {1})".format(
        get_time_1_years_ago(),
        get_time_today(),
    )


def parse_datetime_tuple(s: str) -> Optional[tuple]:
    # Use regex to find all date patterns in the string
    # Matches dates in formats 'YYYY-MM-DD' and 'YYYYMMDD'
    date_pattern = re.compile(r"(\d{4})-?(\d{2})-?(\d{2})")
    dates = date_pattern.findall(s)

    # Process each date and adjust if invalid
    valid_dates = []
    for year_str, month_str, day_str in dates:
        try:
            year, month, day = int(year_str), int(month_str), int(day_str)
            date = datetime.datetime(year, month, day)
            valid_dates.append(date.strftime("%Y-%m-%d"))
        except ValueError:
            # If the date is invalid, adjust to the last day of the month
            # calculate the last day of that month by moving to the first day
            # of the next month and subtracting one day.
            last_day = datetime.datetime(year, month + 1, 1) - datetime.timedelta(
                days=1
            )
            valid_dates.append(last_day.strftime("%Y-%m-%d"))

    # Return as a tuple if two dates are found, otherwise return None
    if len(valid_dates) == 2:
        return tuple(valid_dates)
    else:
        return None

