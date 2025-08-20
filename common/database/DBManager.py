
from http import client
from inspect import ClassFoundException
import re
import importlib

class DBManager:
    '''
    Generic class for database access.
    '''
    _clients = {}
    _functions = {}
    
    def get_client(self, import_string:str): 
        return self._clients[import_string]
    
    @classmethod
    def connect(cls, 
                import_string:str, 
                db_config:dict, 
                #Arguments after this line are the input arguments for the database client constructor.
                **kwargs
                ): 
        if import_string not in cls._clients:
            found = re.search(r'from (.*) import (.*)', import_string)
            msg = f'{import_string} failed'
            if found:
                m = __import__(found.group(1), fromlist=[found.group(2)])
                m = getattr(m, found.group(2))
                print(f'Connecting to database')
                print(m)
                print(kwargs) 
                obj = m(**kwargs)
                db = obj.get_database(db_config['client']['db-name'])  
                cls._clients[import_string] = obj
                methods = [name for name in dir(obj) if callable(getattr(obj, name))]
                for method in methods:
                    key = f'{import_string}.{method}'
                    cls._functions[key] = getattr(obj, method)
                return obj
            else:
                msg = f'Class {m} not found'
            raise Exception(msg)
        else:
            return cls._clients[import_string] 
        
    
    
    @classmethod
    def execute(cls, class_name:str, function_name:str, *args, **kwargs):
        """_summary_

        Args:
            class_name (str): Name of the database client class (ie. MongoClient)
            function_name (str): The name of the function in the class class_name to be used (ie. insert_one)
            *args : Arguments of the function function_name
            **kwargs: Arguments of the function function_name
        """
        key = f'{class_name}.{function_name}'
        if key in cls._functions:
            cls._functions[key](*args, **kwargs)
        else:
            raise AttributeError(f'Function {function_name} not found')
        