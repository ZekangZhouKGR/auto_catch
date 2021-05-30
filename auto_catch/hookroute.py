import time
import logging

import threading
from queue import Queue 

import PyHook3 as pyHook
import pythoncom
import win32con

logger = logging.getLogger(__name__)


class HookRoute(threading.Thread):
    """docstring for HookRoute"""
    def __init__(self):
        super(HookRoute, self).__init__()
        self.__stop = False
        self.__queue_list = []
        self.__handle_list = []

    def run(self):
        hm = pyHook.HookManager()
        hm.KeyAll = self.onKeyboardEvent
        hm.MouseAll = self.onMouseEvent
        hm.HookKeyboard()
        hm.HookMouse()
        pythoncom.PumpMessages()

    def stop(self):
        self.__stop = True

    def get_channel(self):
        queue = Queue(maxsize=0)
        self.__queue_list.append(queue)
        return queue

    def keyboard_handle(self, event):
        return True

    def mouse_handle(self, event):
        return True

    def onKeyboardEvent(self, event):
        for queue in self.__queue_list:
            queue.put(event)

        return self.keyboard_handle(event)

    def onMouseEvent(self, event):
        if event.MessageName != 'mouse move':        
            for queue in self.__queue_list:
                    queue.put(event)

        return self.mouse_handle(event)


class HookLogger(threading.Thread):
    """
    docstring for HookLogger

    https://wiki.winehq.org/List_Of_Windows_Messages
    """
    _mouse_event_map = {
        win32con.WM_LBUTTONDOWN: 'left',
        win32con.WM_RBUTTONDOWN: 'right',
        win32con.WM_MBUTTONDOWN: 'middle',
        win32con.WM_LBUTTONUP: 'left',
        win32con.WM_RBUTTONUP: 'right',
        win32con.WM_MBUTTONUP: 'middle',
    }


    def __init__(self, queue):
        super(HookLogger, self).__init__()
        self.queue = queue
        self. _current_status = set()

    def run(self):
        while True:
            event = self.queue.get()
            self.change_status(event)

    def change_status(self, event):
        current_status = self._current_status
        mouse_event_map = self._mouse_event_map

        if event.Message in (win32con.WM_LBUTTONDOWN, win32con.WM_RBUTTONDOWN, win32con.WM_MBUTTONDOWN):
            if event.Message in mouse_event_map.keys():
                current_status.add(mouse_event_map[event.Message])

        elif event.Message in (win32con.WM_LBUTTONUP, win32con.WM_RBUTTONUP, win32con.WM_MBUTTONUP):
            if event.Message in mouse_event_map.keys():
                event = mouse_event_map[event.Message]

                if event in current_status:
                    current_status.remove(event)

        elif event.Message == win32con.WM_KEYUP:
            if event.ScanCode in current_status:
                current_status.remove(event.ScanCode)

        elif event.Message == win32con.WM_KEYDOWN:
            current_status.add(event.ScanCode)
        

class HotKey(HookRoute):
    """docstring for HotKey"""

    __hotkey = {}

    def __init__(self):
        super(HotKey, self).__init__()

    def run(self):
        self.hookLogger = HookLogger(None)
        self.hookLogger.setDaemon(True)
        super(HotKey, self).run()

    def regist_hotkey(self, when, before, after):
        before = frozenset(before)
        after = frozenset(after)
        queue = Queue()
        self.__hotkey[(when, before, after)] = queue
        logger.info('regist_hotkey hotkey %s -> %s when %d', before, after, when)
        return queue

    def onEvent(self, event):
        when = event.Message
        before = frozenset(self.hookLogger._current_status)
        self.hookLogger.change_status(event)
        after = frozenset(self.hookLogger._current_status)
        status = (when, before, after)

        if after != before:
            logger.debug('%s -> %s at %s', before, after, when)

        if (when, before, after) in self.__hotkey.keys():
            logging.info('%s -> %s at %s', before, after, when)
            queue = self.__hotkey[(when, before, after)]
            queue.put(event)
            return False

        else:
            return True

    def onKeyboardEvent(self, event):
        super(HotKey, self).onKeyboardEvent(event)
        return self.onEvent(event)

    def onMouseEvent(self, event):
        super(HotKey, self).onMouseEvent(event)
        return self.onEvent(event)

def main():

    # 创建管理器
    logging.basicConfig(level=logging.DEBUG)

    hotkey = HotKey()
    hotkey.regist_hotkey(win32con.WM_KEYDOWN, {}, {30})
    hotkey.setDaemon(True)
    hotkey.start()
    while True:
        try:
            time.sleep(4)
        except KeyboardInterrupt as e:
            break
 
if __name__ == "__main__":
    main()
