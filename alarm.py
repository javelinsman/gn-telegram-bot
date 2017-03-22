import threading
import time
from convert import byte2str


#TODO :  _id
class Alarm:
    def __init__(self, active_wday, tm_hour, tm_min, cid, msg):
        self.active_wday = active_wday
        self.tm_hour = tm_hour
        self.tm_min = tm_min
        self.cid = cid
        self.msg = msg
    def __str__(self):
        return '@\0@'.join([
            ''.join(map(lambda x:'T' if x else 'F', self.active_wday)),
            str(self.tm_hour), str(self.tm_min), str(self.cid), str(self.msg)
        ])
    def parse(serial):
        str_wday, tm_hour, tm_min, cid, msg = serial.split('@\0@')
        active_wday = list(map(lambda x:True if x == 'T' else False, str_wday))
        tm_hour, tm_min, cid = map(int, [tm_hour, tm_min, cid])
        return Alarm(active_wday, tm_hour, tm_min, cid, msg)

class AlarmThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
    def __init2__(self):
        self.db = self.singleton.db
        self.sender = self.singleton.threads["sender"]
    def th_exit(self):
        self.__exit = True
    def run(self):
        while not self.__exit:
            if self.db.llen('gn:alarm:list-alarm') > 0:
                alarm_list = map(byte2str, self.db.lrange('gn:alarm:list-alarm', 0, -1))
                for alarm_str in alarm_list:
                    alarm = Alarm.parse(alarm_str)
                    now = time.localtime(time.time())
                    if alarm.tm_hour == now.tm_hour and alarm.tm_min == now.tm_min:
                        visited_key = 'gn:alarm:visited:%s' % alarm_str
                        if self.db.get(visited_key) is None:
                            self.db.set(visited_key, 1)
                            self.db.expire(visited_key, 600)
                            self.sender.add_by_cid_msg(alarm.cid, alarm.msg)
            time.sleep(10)
