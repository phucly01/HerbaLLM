
from io import BytesIO
import openpyxl
from data_collector.parsers.Parser import Parser
from data_collector.storage.Storage import Storage
import importlib as imp


class tcmbankcnDownloadParser(Parser):
        
    def parse(self, filename, data):
        if not hasattr(self, 'storage'):
            self.storage = self.storage_class(self.config, filename)
            
        bio = BytesIO(data)
        category_map = self.config['parser']['categories']
        category = None
        for map in category_map:
            if filename in map:
                category = map[filename]
                break
        parserclass = Parser.get_data_parser(category)
        if parserclass:
            print(f'### Parsing {filename}')
            parserclass().process(bio, map['data-selector'], self.storage)
        bio.close()