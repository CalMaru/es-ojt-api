from abc import ABCMeta, abstractmethod


class KeywordService(metaclass=ABCMeta):
    @abstractmethod
    def autocomplete(self, query, key, index, es_client):
        pass
