import threading
import time
from convert import byte2str

# Here I use @\0@ as delimiter to ensure it never included in user input

class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
    def __init2__(self):
        self.db = self.singleton.db
    def th_exit(self):
        self.__exit = True
    def run(self):
        while not self.__exit:
            while self.db.llen('gn:timer:list-event') > 0:
                event = byte2str(self.db.lindex('gn:timer:list-event', 0))
                e_time, e_chan, e_cont = event.split('@\0@')
                if float(e_time) < time.time():
                    self.db.lpop('gn:timer:list-event')
                    self.db.publish(e_chan, e_cont)
                else:
                    break
            time.sleep(1)
    def add_event(self, time, channel, content):
        event = '%s@\0@%s@\0@%s' % (time, channel, content)
        self.db.rpush('gn:timer:list-event', event)
