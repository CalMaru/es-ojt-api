from abc import ABCMeta, abstractmethod


class SearchService(metaclass=ABCMeta):
    @abstractmethod
    def search(self, es_client):
        pass
