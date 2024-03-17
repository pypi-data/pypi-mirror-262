from abc import ABC, abstractmethod

class DictHandler(ABC):
    @abstractmethod
    def query(self, word):
        pass

    # add
    # update
    # remove
    # export
