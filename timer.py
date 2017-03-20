import threading
import queue
import time
from convert import byte2str

class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
    def th_exit(self):
        self.__exit = True
    def run(self):
        while not self.__exit:
            while True:
                event = self.singleton.db.lindex('gn:timer:list-event', 0)
                e_time, e_chan, e_cont = event.split(':')
                if float(e_time) < time.time():
                    self.singleton.db.publish(e_chan, e_cont)
                else:
                    break
            time.sleep(1)
    def add_event(self, time, channel, content):
        event = '%s:%s:%s' % (time, channel, content)
        self.singleton.db.rpush('gn:timer:list-event', event)
