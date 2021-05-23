import time
import mylogging
import threading

import win32con
from airtest.core.api import init_device

from auto_catch import mylogging
from auto_catch.config import ConfigParser
from auto_catch.units import Snapshot
from auto_catch.hookroute import HotKey


class ClickToSnapshot(threading.Thread):
    """docstring for ClickToSnapshot"""

    def __init__(self, queue):
        super(ClickToSnapshot, self).__init__()
        self.queue = queue
        self.snapshot = Snapshot()

    def run(self):
        while True:
            event = self.queue.get()
            point = event.Position
            self.snapshot.crop_screen_by_point(point)
        

def main(ap):
    init_device(platform="Windows")
    config = ConfigParser()

    hotkey = HotKey()
    hotkey.setDaemon(True)
    hotkey.start()

    channel = hotkey.regist_hotkey(win32con.WM_LBUTTONDOWN, {29}, {'left', 29})

    cts = ClickToSnapshot(channel)
    cts.setDaemon(True)
    cts.start()
    while True:
        try:
            time.sleep(4)
        except KeyboardInterrupt as e:
            break

if __name__ == '__main__':
    main(None)