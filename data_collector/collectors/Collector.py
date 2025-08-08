

import abc
from data_collector.parsers.Parser import Parser


class Collector(abc.ABC):
    
    def __init__(self, config, parserclass, storageclass):
        self.parser_class = parserclass
        self.storage_class = storageclass
        self.config = config
    
    @abc.abstractmethod
    def collect(self, url:str, user:str=None, passwd:str=None)->bool:
        raise NotImplementedError