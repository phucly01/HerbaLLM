
import re
import typing
from config.Config import Config
import importlib as imp


class DataCollector:
    
    sources : typing.ClassVar = Config().collectors['sources']
    
    def collect(self):
        for source in self.sources:
            url = source["url"]
            user = source["user"] if "user" in source else None
            password = source["password"] if "password" in source else None
            print(f'Collecting data from {url}')
            #classname = re.search(r'.*//([^?]+)', url).group(1)  #classname is derived from the url, between // and ? exclusive.
            classname = 'tcmbankcnDownload'
            classname = ''.join([c for c in classname if c.isalpha() or c.isdigit()])  #Keep only alphabet letters and numbers
            collectorclassname = f'data_collector.collectors.{classname}Collector'
            parserclassname = f'data_collector.parsers.{classname}Parser'
            storageclassname = f'data_collector.storage.{classname}Storage'
            print(f'Collector classes: {collectorclassname} {parserclassname} {storageclassname}')
            collectormodule = imp.import_module(collectorclassname)
            parsermodule = imp.import_module(parserclassname)
            
            try:
                storagemodule = imp.import_module(storageclassname)
                storageclass = getattr(storagemodule, f'{classname}Storage')
            except ModuleNotFoundError:   #If specific class is not found, use the default super class
                storagemodule = imp.import_module('data_collector.storage.Storage')
                storageclass = getattr(storagemodule, 'Storage')
                
            parserclass = getattr(parsermodule, f'{classname}Parser')
            collectorclass = getattr(collectormodule, f'{classname}Collector')
            
            collector = collectorclass(source, parserclass, storageclass)
        
            collector.collect(url, user, password)
            