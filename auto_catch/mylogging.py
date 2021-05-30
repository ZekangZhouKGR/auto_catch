import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

root = logging.getLogger('auto_catch')
root.setLevel(logging.DEBUG)

logging.info('start logging with {} level'.format(root.level))
