from app.rpc_server.message_listener import PikaListener


@PikaListener()
class MQService(object):
    def __init__(self):
        super().__init__()
