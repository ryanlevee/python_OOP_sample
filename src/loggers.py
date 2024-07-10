import logging

from interfaces import ILogger

logging.basicConfig(level=logging.DEBUG)


class EventLogger(ILogger):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)
