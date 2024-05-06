from abc import ABCMeta, abstractmethod


class AutocompleteService(metaclass=ABCMeta):
    @abstractmethod
    def get_reporters(self, query, es_client):
        pass

    @abstractmethod
    def get_news_keywords(self, query, es_client):
        pass
