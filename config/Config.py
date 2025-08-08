
import yaml
import os

class Config:
    settings = None
    collectors = None
    
    @classmethod
    def __init__(cls):
        if not cls.settings:
            with open(f'{os.path.dirname(os.path.abspath(__file__))}/settings.yaml', 'r') as file:
                cls.settings = yaml.safe_load(file)
        if not cls.collectors:
            with open(f'{os.path.dirname(os.path.abspath(__file__))}/collectors.yaml', 'r') as file:
                cls.collectors = yaml.safe_load(file)