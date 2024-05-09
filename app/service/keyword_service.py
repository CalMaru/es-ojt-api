from abc import ABCMeta, abstractmethod


class KeywordService(metaclass=ABCMeta):
    @abstractmethod
    def autocomplete(self, query, key, index, es_client):
        pass

    @abstractmethod
    def is_terms_exist(self, query, es_client):
        pass
