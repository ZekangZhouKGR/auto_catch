# -*- encoding=utf8 -*-
import os
import json
import logging
import threading

from airtest.core.api import G
from airtest.aircv import aircv

from datetime import datetime

logger = logging.getLogger(__name__)


class Snapshot(object):
    """docstring for snapshot"""

    def __init__(self, basedir = './image'):
        super(Snapshot, self).__init__()
        self.basedir = basedir

    def crop_screen_by_point(self, point):
        screen = self.snapshot()

        if not os.path.isdir(self.basedir):
            os.makedirs(self.basedir)

        dirname = datetime.now().strftime('%Y%m%d_%H%M%S.%f')
        dirpath = os.path.join(self.basedir, dirname)
        if not os.path.isdir(dirname):
            os.makedirs(dirpath)

        filepath = os.path.join(dirpath, 'full.jpg')
        logger.info('save image to %s', filepath)
        self.save_image(filepath, screen)
        self.write_meta_data(dirpath, dirname, screen, point)

        for size in (16, 32, 64):
            x = point[0]
            y = point[1]
            image = self.crop_image(screen, 
                (x - size, y - size, x + size, y + size))

            filepath = os.path.join(dirpath, str(size) + '.jpg')
            self.save_image(filepath, image)


    @staticmethod
    def write_meta_data(dirpath, time, screen, point):
        meta = {
            'src': point,
            'screen': screen.shape,
            'time': time
        }

        filename = os.path.join(dirpath, 'meta.json')
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(meta, f)

    @staticmethod
    def snapshot():
        screen = G.DEVICE.snapshot(quality = 100)
        return screen
    
    @staticmethod
    def crop_image(screen, rect):
        screen = aircv.crop_image(screen, rect)
        return screen

    @staticmethod
    def save_image(filepath, image):
        aircv.imwrite(filepath, image, quality = 99)