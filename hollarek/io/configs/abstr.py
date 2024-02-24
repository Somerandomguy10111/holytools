from abc import abstractmethod
from hollarek.dev import get_logger, LogSettings

Settings = dict[str, str]


class Configs:
    def __init__(self):
        self._settings : Settings = {}
        logger = get_logger(settings=LogSettings(), name=self.__class__.__name__)
        self.log = logger.log


    def get(self, key : str) -> str:
        try:
            value = self._settings.get(key)
            if not value:
                raise KeyError
        except Exception as e:
            value = input(f'Could not find key {key} in settings: \"{e}\" Please set it manually')
            value = self.set(key=key, value=value)
        return value


    @abstractmethod
    def retrieve_settings(self):
        pass


    @abstractmethod
    def set(self, key : str, value : str):
        pass
