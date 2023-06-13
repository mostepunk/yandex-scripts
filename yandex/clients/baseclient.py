from abc import abstractmethod


class BaseClient:
    def __init__(self):
        self.client = self.__class__.__name__

    @abstractmethod
    def files(self, folder: str):
        pass
