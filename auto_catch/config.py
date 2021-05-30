import sys
import os
import logging

from pyCommon.config import ConfigParser as BaseConfigParser

logger = logging.getLogger(__name__)

class ConfigParser(BaseConfigParser):
    """docstring for ConfigParser"""
    LOCAL_PATH = './config.ini'
    USER_PATH = ['.config', 'auto_catch', 'config.ini']
        
        
def main(ap):
    config = ConfigParser()


if __name__ == '__main__':
    main(None)