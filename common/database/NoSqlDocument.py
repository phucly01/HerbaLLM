import uuid
import typing

from numpy import isin
import pydantic
import pymongo
import abc
from common.database.DBManager import DBManager
from config.Config import Config


NoSqlDoc = typing.TypeVar('NoSqlDoc', bound='NoSqlDocument')

class NoSqlDocument(pydantic.BaseModel, typing.Generic[NoSqlDoc], abc.ABC):
    """
    Base class for all NoSQL documents
    """    
    # config : typing.ClassVar = Config().settings['data_collector']['storage']
     
    class Config:
        arbitrary_types_allowed = True

    table_name: str = ''
    # db_manager: DBManager = None
        
    
    def __eq__(self, obj:object) -> bool:
        return isinstance(obj, self.__class__) and self.id == obj.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    #This is called automatically after the __init__()
    # def model_post_init(self, ctx):
        # if not self.db_manager:
        #     import_string = self.config['client']['import_string']
        #     self.db_manager = DBManager()
        #     self.db_manager.connect(import_string, self.config['client']['url'])
    
    def to_db_data(self: NoSqlDoc, _id_col_name, **kwargs) -> dict:
        dump = self.model_dump(
            exclude_unset=kwargs.pop('exclude_unset', False),
            by_alias=kwargs.pop('by_alias', True), 
            **kwargs)
        
        #BaseModel compatibility:
        if _id_col_name in dump:
            dump['_id'] = str(dump.pop(_id_col_name))
        return dump
    
    @classmethod
    def to_document(cls: typing.Type[NoSqlDoc], _id_col_name, data:dict) -> NoSqlDoc|None:
        if not data:
            return None
        data[_id_col_name] = data.pop('_id')
        return cls(**dict(data))
    
    # def get_db_name(self) -> str:
    #     return self.config['client']['db-name']
    
    # def set_table_name(self, table_name):
    #     self.table_name = table_name
    
    # def get_table_name(self) -> str:
    #     return self.table_name  #Must be set using constructor
    
    # def save(self:NoSqlDoc, data:list) -> bool:
    #     if not data:
    #         return False 
    #     if len(data) == 1:
    #         self.db_manager.execute(self.config['client']['import_string'], self.config['client']['functions']['update'], self.get_db_name(),  data[0]) 
    #     else:
    #         self.db_manager.execute(self.config['client']['import_string'], self.config['client']['functions']['update_many'], self.get_db_name(), data) #Todo move the function name to setting for generalization
    #     return True
        