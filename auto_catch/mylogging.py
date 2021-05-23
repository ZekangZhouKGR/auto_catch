import logging
import sys

logging.basicConfig(level = logging.INFO,
    format = '%(asctime)s.%(msecs)03d [%(levelname)5s] %(filename)s:%(lineno)d %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    stream = sys.stdout)
