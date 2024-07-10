from abc import ABC, abstractmethod


class IDatabaseOperation(ABC):
    @abstractmethod
    def execute(self):
        pass


class ISoapOperation(ABC):
    @abstractmethod
    def execute(self):
        pass


class IConnectionHolder(ABC):
    @abstractmethod
    def get_conn(self):
        pass

    def get_cnxn_cur(self):
        pass


class IDataProcessor(ABC):
    @abstractmethod
    def process(self):
        pass


class ILogger(ABC):
    @abstractmethod
    def log_debug(self, message):
        pass

    @abstractmethod
    def log_info(self, message):
        pass

    @abstractmethod
    def log_error(self, message):
        pass
