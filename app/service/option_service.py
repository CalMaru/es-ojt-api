from abc import ABCMeta, abstractmethod


class OptionService(metaclass=ABCMeta):
    @abstractmethod
    def get_options(self, es_client):
        pass
