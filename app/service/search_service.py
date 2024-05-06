from abc import ABCMeta, abstractmethod


class SearchService(metaclass=ABCMeta):
    @abstractmethod
    def search(self, request, es_request, es_client):
        pass
