from abc import ABCMeta, abstractmethod


class ProviderService(metaclass=ABCMeta):
    @abstractmethod
    def get_providers(self):
        pass
