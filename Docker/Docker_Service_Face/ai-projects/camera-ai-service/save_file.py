import logging


class TestLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestLogger, cls).__new__(cls)
            # Initialize only once
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger("test_logger")
            self.logger.setLevel(logging.DEBUG)

            # Prevent adding multiple handlers
            if not self.logger.handlers:
                file_handler = logging.FileHandler("/tmp/test_dahua.log")
                file_handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

            self._initialized = True

    def get_logger(self):
        return self.logger

    def log(self, message):
        self.logger.debug(message)


# Log messages
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')

# If you also want to log to the console, you can add a stream handler
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
#
# # Example usage
# logger.info('This message will be logged to both the file and the console')
