from abc import ABCMeta, abstractmethod


class CategoryService(metaclass=ABCMeta):
    @abstractmethod
    def get_categories(self):
        pass
