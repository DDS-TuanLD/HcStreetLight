from abc import ABC, ABCMeta, abstractmethod


class IController(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        return
