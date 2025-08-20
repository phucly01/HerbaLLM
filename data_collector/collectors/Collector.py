

import abc
from data_collector.parsers.Parser import Parser


class Collector(abc.ABC):
    
    def __init__(self, config, parserclass, storageclass):
        self.parser_class = parserclass
        self.storage_class = storageclass
        self.config = config
    
    @abc.abstractmethod
    def collect(self, url:str, user:str=None, passwd:str=None)->list:
        """Entrance function to data collector module.  It gathers the data from the specified url or file, parse them, and store to nosql database.

        Args:
            url (str): An URL or file path
            user (str, optional): username for the specified URL (site). Defaults to None.
            passwd (str, optional): password for the specified URL (site). Defaults to None.

        Raises:
            NotImplementedError: This is raised by the base class only.  The subclass should implement this method, hence no NotImplementedError exception

        Returns:
            list: A list of returns, each element represent the result of each suburl (if applicable) within the main URL.  If it only a single URL, this returns a list of 1.  None = success, non-None = error
        """
        raise NotImplementedError