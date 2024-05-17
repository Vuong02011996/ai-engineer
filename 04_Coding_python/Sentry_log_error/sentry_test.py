import sentry_sdk
from sentry_sdk import capture_exception, Hub
sentry_sdk.init("http://8886fd3bd10c418ab14900923854b20a@192.168.111.98:9000/2")

try:
    print(1/0)
except Exception as e:
    # Alternatively the argument can be omitted
    capture_exception(e)
    pass

