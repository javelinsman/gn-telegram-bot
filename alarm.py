import threading
import time
from convert import byte2str

class Alarm:
    def __init__(self, active_wday, tm_hour, tm_min, name=None, tag=None):
        self.active_wday = active_wday
        self.tm_hour = tm_hour
        self.tm_min = tm_min
        self.name = name
        self.tag = tag
    def __str__(self):
        return '@\0@'.join([
            ''.join(map(lambda x:'T' if x else 'F', self.active_wday)),
            str(self.tm_hour), str(self.tm_min),
            str(self.name), str(self.tag)
        ])
    def parse(serial):
        str_wday, tm_hour, tm_min, name, tag = serial.split('@\0@')
        active_wday = list(map(lambda x:True if x == 'T' else False, str_wday))
        tm_hour, tm_min = map(int, [tm_hour, tm_min])
        name = name if name != 'None' else None
        tag = tag if tag != 'None' else None
        return Alarm(active_wday, tm_hour, tm_min, name, tag)

"""
class AlarmThread(threading.Thread):
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
"""
