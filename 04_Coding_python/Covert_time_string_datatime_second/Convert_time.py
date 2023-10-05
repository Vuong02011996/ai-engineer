
"""
Always compare with epoch time
"""

import time
from datetime import datetime


def convert():

    # Get time now with timezone
    time_now = datetime.now()
    print("time_now: ", time_now)
    # Get time now with utc
    time_now_utc = datetime.utcnow()
    print("time_now_utc: ", time_now_utc)

    # format_time = "%Y-%m-%dT%H:%M:%S.%fZ" # time utc
    # format_time = '%Y-%m-%dT%H:%M:%S%z'  # time zone
    format_time = '%Y-%m-%dT%H:%M:%S'  # time zone

    # Convert datetime to string time
    string_time = time_now.strftime(format_time)
    # string_time = time_now_utc.strftime(format_time)

    """
    # time_now
    time_now:  2022-04-09 09:46:26.387949
    time_now_utc:  2022-04-09 02:46:26.387968
    string_time:  "2022-04-09T09:46:26"
    time_dt:  2022-04-09 09:46:26
    time_s:  1649472386.0
    
    # time_now_utc
    time_now:  2022-04-09 09:47:46.238913
    time_now_utc:  2022-04-09 02:47:46.238939
    string_time:  "2022-04-09T02:47:46"
    time_dt:  2022-04-09 02:47:46
    time_s:  1649447266.0

    """
    print("string_time: ", string_time)

    # Convert string time to datetime
    time_dt = datetime.strptime(string_time, format_time)
    print("time_dt: ", time_dt)

    # Convert datetime to second time
    time_s = time_dt.timestamp()

    print("time_s: ", time_s)


if __name__ == '__main__':
    convert()
