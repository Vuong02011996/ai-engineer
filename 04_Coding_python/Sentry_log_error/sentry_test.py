
from sentry_sdk import capture_exception, capture_message
import sentry_sdk
from datetime import datetime
import os
cwd = os.getcwd()

import traceback

sentry_sdk.init(
    dsn="http://8886fd3bd10c418ab14900923854b20a@192.168.111.98:9000/2",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
)
# module_name = str(cwd)
# ip_service = "192.168.111.98"
# time_error = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# capture_message(f"[Face].[192.168.111.11][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}].[]")
try:
    print(1/0)
except Exception as e:
    # Alternatively the argument can be omitted
    # capture_exception(e)
    print(traceback.format_exc())
    print(str(e).upper())
    capture_message(f"[FACE][192.168.111.11][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
    pass

