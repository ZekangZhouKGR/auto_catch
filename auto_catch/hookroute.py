import time
import logging
from copy import deepcopy

import threading
from queue import Queue 

import PyHook3 as pyHook
import pythoncom
import win32con

logger = logging.getLogger(__name__)

class HookStatus():

    mouse_down_set = {win32con.WM_LBUTTONDOWN, win32con.WM_RBUTTONDOWN, win32con.WM_MBUTTONDOWN}
    mouse_up_set = {win32con.WM_LBUTTONUP, win32con.WM_RBUTTONUP, win32con.WM_MBUTTONUP}
    mouse_cov = {
        win32con.WM_LBUTTONUP: win32con.WM_LBUTTONDOWN,
        win32con.WM_RBUTTONUP: win32con.WM_RBUTTONDOWN,
        win32con.WM_MBUTTONUP: win32con.WM_MBUTTONDOWN
    }

    def __init__(self, keyboard_status = None, mouse_status = None):
        keyboard_status = keyboard_status if keyboard_status else set()
        mouse_status = mouse_status if mouse_status else set()
        self.__keyboard_status = keyboard_status
        self.__mouse_status = mouse_status
        self.position = (0, 0)

    def change_status(self, event):

        if event.Message in self.mouse_down_set:
            self.__mouse_status.add(event.Message)
            self.position = event.Position

        elif event.Message in self.mouse_up_set:
            cov_status = self.mouse_cov[event.Message]
            self.__mouse_status.remove(cov_status)
            self.position = event.Position

        elif event.Message == win32con.WM_KEYUP:
            if event.ScanCode in self.__keyboard_status:
                self.__keyboard_status.remove(event.ScanCode)

        elif event.Message == win32con.WM_KEYDOWN:
            self.__keyboard_status.add(event.ScanCode)

    def freeze(self):
        return (
            frozenset(self.__keyboard_status),
            frozenset(self.__mouse_status),
        )

    def __str__(self):
        return '[%s, %s, %s]' % (self.__keyboard_status, self.__mouse_status, self.position)


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

    """

    def __init__(self, queue):
        super(HookLogger, self).__init__()
        self.queue = queue
        self._current_status = HookStatus({}, {})

    def run(self):
        while True:
            event = self.queue.get()
            self.change_status(event)

    def change_status(self, event):
        self._current_status.change_status(event)


class HotKey(HookRoute):
    """docstring for HotKey"""

    __hotkey = {}

    def __init__(self):
        super(HotKey, self).__init__()
        self._hook_status = HookStatus({}, {})

    def run(self):
        super(HotKey, self).run()

    def regist_hotkey(self, when, before, after, channel = None):
        queue = Queue() if channel is None else channel
        before = before.freeze()
        after = after.freeze()
        self.__hotkey[(when, before, after)] = queue
        logger.info('regist_hotkey hotkey %s -> %s when %d', before, after, when)
        return queue

    def onEvent(self, event):
        when = event.Message
        before = self._hook_status.freeze()
        self._hook_status.change_status(event)
        after = self._hook_status.freeze()
        status_chain = (when, before, after)

        if after != before:
            logger.debug('%s -> %s at %s', before, after, when)

        if status_chain in self.__hotkey.keys():
            logging.info('%s -> %s at %s', before, after, when)
            queue = self.__hotkey[status_chain]
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
