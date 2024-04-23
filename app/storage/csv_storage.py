from abc import ABCMeta, abstractmethod


class CSVStorage(metaclass=ABCMeta):
    @abstractmethod
    def read_csv(self, file_path):
        pass
