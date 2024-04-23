from abc import ABCMeta, abstractmethod


class SearchService(metaclass=ABCMeta):
    @abstractmethod
    def get_providers(self, provider_type):
        pass
