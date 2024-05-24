import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import socket

sentry_sdk.capture_message("Check full error")
# Get IP address and hostname
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

sentry_logging = LoggingIntegration(
    level=None,  # Capture info and above as breadcrumbs
    # event_level='error'  # Send errors as events
)


def before_send(event, hint):
    event['extra']['custom_info'] = 'Additional custom information'
    return event


sentry_sdk.init(
    dsn="http://8886fd3bd10c418ab14900923854b20a:b0f95cdba5d64a928d4bc8f31f11d3fb@192.168.111.98:9000/2",
    # integrations=[sentry_logging],
    environment="production",
    release="your_app@1.0.0",
    attach_stacktrace=True,
    before_send=before_send,
)


sentry_sdk.set_context("hardware", {
    "ip": ip_address,
    "host": hostname
})

sentry_sdk.set_tag("service", "web")

try:
    # Code that may raise an exception
    print(1 / 0)
except Exception as error:
    sentry_sdk.add_breadcrumb(
        category='example',
        message='An example breadcrumb',
        level='info',
    )
    sentry_sdk.capture_exception(error)
    sentry_sdk.set_context("custom_context", {
        "info": "Additional info about this error",
        "user_id": "1234",
        "transaction_id": "abcd"
    })
