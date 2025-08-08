import abc

from data_collector.storage.Storage import Storage

class Category(abc.ABC):
    
    
    abc.abstractmethod
    def process(self, data, data_selector:list, storage:Storage):
        raise NotImplementedError
    