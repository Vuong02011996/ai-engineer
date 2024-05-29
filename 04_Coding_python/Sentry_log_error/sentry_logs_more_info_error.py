import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import socket

# Get IP address and hostname
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

sentry_logging = LoggingIntegration(
    level=None,  # Capture info and above as breadcrumbs
    # event_level='error'  # Send errors as events
)

def before_send(event, hint):
    # Add extra information to the event
    event['extra']['custom_info'] = 'Additional custom information'
    return event

sentry_sdk.init(
    dsn="http://b0c893091b583712997730492a86ac6c@192.168.111.98:9000/2",
    integrations=[sentry_logging],
    environment="production",
    release="your_app@1.0.0",
    attach_stacktrace=True,
    before_send=before_send,
)

sentry_sdk.capture_message("Error1")
# Setting global context using set_context
sentry_sdk.set_context("hardware", {
    "ip": ip_address,
    "host": hostname
})

try:
    # Code that may raise an exception
    1 / 0
except Exception as error:
    sentry_sdk.add_breadcrumb(
        category='example',
        message='An example breadcrumb',
        level='info',
    )
    # Setting additional context before capturing the exception
    sentry_sdk.set_context("custom_context", {
        "info": "Additional info about this error",
        "user_id": "1234",
        "transaction_id": "abcd"
    })
    sentry_sdk.capture_exception(error)