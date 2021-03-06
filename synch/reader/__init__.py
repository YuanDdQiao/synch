import abc
import logging
import signal
from signal import Signals
from typing import Callable, Tuple, Union

from synch.broker import Broker
from synch.settings import Settings

logger = logging.getLogger("synch.reader")


class Reader:
    cursor = None
    fix_column_type = False

    def __init__(self, settings: Settings):
        self.settings = settings
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def execute(self, sql, args=None):
        logger.debug(sql)
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    @abc.abstractmethod
    def get_primary_key(self, db: str, table: str) -> Union[None, str, Tuple[str, ...]]:
        raise NotImplementedError

    @abc.abstractmethod
    def start_sync(self, broker: Broker):
        raise NotImplementedError

    @abc.abstractmethod
    def signal_handler(self, signum: Signals, handler: Callable):
        raise NotImplementedError
