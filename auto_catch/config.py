import sys
import os
import logging

from configparser import ConfigParser as BaseConfigParser

class ConfigParser(BaseConfigParser):
    """docstring for ConfigParser"""
    LOCAL_PATH = './config.ini'
    # USER_PATH = './config.ini'
    # SYSTEM_PATH = './config.ini'

    def __init__(self):
        super(ConfigParser, self).__init__()
        self._set_default()
        self.safe_read(self.LOCAL_PATH)

    def safe_read(self, path):
        if os.path.isfile(path):
            try:
                self.read(path)
                return True
            except Exception as e:
                logging.warning('failed to load %s', path)
        return False

    def read(self, path):
        logging.info('read config from %s', path)
        super(ConfigParser, self).read(path)

    def _set_default(self):
        pass
        
        
def main(ap):
    config = ConfigParser()


if __name__ == '__main__':
    main(None)