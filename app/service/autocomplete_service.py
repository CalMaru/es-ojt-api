from abc import ABCMeta, abstractmethod


class AutocompleteService(metaclass=ABCMeta):
    @abstractmethod
    def autocomplete(self, query, query_type):
        pass
