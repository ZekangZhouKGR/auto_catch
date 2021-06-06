import sys
import logging
import time
import threading

import win32con
from airtest.core.api import init_device

from auto_catch.config import ConfigParser
from auto_catch.units import Snapshot
from auto_catch.hookroute import HotKey
from auto_catch.hookroute import HookStatus
from auto_catch.common import console_entry


logger = logging.getLogger(__name__)


class ClickToSnapshot(threading.Thread):
    """docstring for ClickToSnapshot"""

    def __init__(self, queue):
        super(ClickToSnapshot, self).__init__()
        self.queue = queue
        self.snapshot = Snapshot()

    def run(self):
        while True:
            event = self.queue.get()
            if hasattr(event, 'ScanCode'):
                break

            point = event.Position
            self.snapshot.crop_screen_by_point(point)
        
def initArgumentParser(ap):
    return ap

@console_entry(initArgumentParser)
def main(ap):

    platform = 'Windows'
    logger.info('start auto_catch in %s...', platform)
    init_device(platform=platform)

    config = ConfigParser()

    hotkey = HotKey()
    hotkey.setDaemon(True)
    hotkey.start()


    logger.info('regist_hotkey ctrl + left to crop image')


    channel = hotkey.regist_hotkey(
        win32con.WM_LBUTTONDOWN, 
        HookStatus({29}), 
        HookStatus({29}, {win32con.WM_LBUTTONDOWN})
    )
    logger.info('regist_hotkey esc to exit')
    channel = hotkey.regist_hotkey(
        win32con.WM_KEYDOWN, 
        HookStatus({}), 
        HookStatus({1}),
        channel
    )

    cts = ClickToSnapshot(channel)
    cts.setDaemon(True)
    cts.start()
    cts.join()

if __name__ == '__main__':
    main(sys.argv[1:])


# 宏 记录 命名 读取 重放
