import logging

LOGGER = logging.getLogger("pika_logger")


class RPCServer:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RPCServer, cls).__new__(cls)
        return cls.instance
