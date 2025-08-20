import abc
from data_collector.storage.Storage import Storage
import importlib as imp


class Parser(abc.ABC):
    
    def __init__(self, config, storageclass):
        self.storage_class = storageclass
        self.config = config
    
    @abc.abstractmethod
    def parse(self, data)->list:
        """Entrance function to parsing module within the data collector module.  It processes the data from the collector, and store to nosql database.

        Args:
            data: raw bytes

        Raises:
            NotImplementedError: This is raised by the base class only.  The subclass should implement this method, hence no NotImplementedError exception

        Returns:
            list: A list of returns, each element represent the result of each suburl (if applicable) within the main URL.  If it only a single URL, this returns a list of 1.  None = success, non-None = error
        """
        raise NotImplementedError 
    
    @staticmethod
    def get_data_parser(category:str=None, 
                        category_map:list=None,
                        filename:str=None
                        ):
        if not category and category_map and filename:
            category = None
            for map in category_map:
                if filename in map:
                    category = map[filename]
                    break
        if not category:
            if not category_map or not filename:
                raise Exception('Incorrect number of arguments.  Specify either category or both category_map and filename')
        try:
            classname = f'{category.title()}Parser'
            parsermodule = f'data_collector.parsers.categories.{classname}'
            print(parsermodule)
            m = imp.import_module(parsermodule)
            parserclass = getattr(m, classname)
            return parserclass
        except Exception as e:
            print(f'No parser found for category {category}')
            return None