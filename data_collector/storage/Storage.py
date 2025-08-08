import abc
from gc import collect
import typing

from common.database.DBManager import DBManager
from config.Config import Config


class Storage(abc.ABC):
    
    config : typing.ClassVar = Config().settings['data_collector']['storage']
    db_manager: DBManager = None
    
    def __init__(self, config, key_map:str):
        self.source = config
        collection_map = self.source['storage']['collections']
        for map in collection_map:
            if key_map in map:
                self.table_name = map[key_map]
                break 
        if not self.db_manager:
            import_string = self.config['client']['import-string']
            self.db_manager = DBManager()
            self.db_manager.connect(import_string, self.config, 
                                    self.config['client']['url'], 
                                    username=self.config['client']['db-user'],
                                    password=self.config['client']['db-pass'],
                                    authSource='admin',
                                    authMechanism='SCRAM-SHA-256')
    
    def get_db_name(self) -> str:
        return self.config['client']['db-name']
    
    def get_table_name(self) -> str:
        return self.table_name   
    
    def save(self, 
             data:list
             ) -> bool:
        """
        Save list of formatted data to database
        Args:
            data (list): This is formatted data where each row is ready to be inserted directly into database collection

        Returns:
            bool: True=success
        """
        if not data:
            return False
        client = self.db_manager.get_client(self.config['client']['import-string'])
        db = client[self.config['client']['db-name']]
        collection = db[self.get_table_name()]
        for d in data:
            collection.replace_one({'_id':d['_id']}, d, upsert=True)
        return True