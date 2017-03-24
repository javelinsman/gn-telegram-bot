import threading
import time
import re
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

class ParseCommand:
    def wday_str_to_bool_list(self, wday):
        names = ['월', '화', '수', '목', '금', '토', '일']
        ret = [False] * 7
        for i, name in enumerate(names):
            ret[i] = name in wday
        return ret
    def wday_bool_list_to_str(self, lst):
        names = ['월', '화', '수', '목', '금', '토', '일']
        ret = ''
        for i, b in enumerate(lst):
            if b:
                ret += names[i]
        return ret
    def __init__(self, msg):
        self.msg = msg
        print('parsing : %s' % self.msg)
        self.args = msg.split()
        self.pat = re.compile('.*"(.*)".*')
    def op_type(self):
        return self.args[0]
    def op_index(self):
        return self.args[1] \
            if self.op_type() in ('삭제', '수정') \
            else None
    def op_blist(self):
        if self.op_type() == '추가':
            return self.wday_str_to_bool_list(self.args[1])
        elif self.op_type() == '수정':
            return self.wday_str_to_bool_list(self.args[2])
    def op_time(self):
        if self.op_type() == '추가':
            return map(int, self.args[2].split(':'))
        elif self.op_type() == '수정':
            return map(int, self.args[3].split(':'))
    def op_cid(self):
        if self.op_type() == '추가':
            return int(self.args[3])
        elif self.op_type() == '수정':
            return int(self.args[4])
    def op_msg(self):
        if self.op_type() in ('추가', '수정'):
            return self.pat.match(self.msg).group(1)
    def argpack_add(self):
        return (self.op_blist(), *self.op_time(), self.op_cid(), self.op_msg())

class AlarmThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
    def __init2__(self):
        self.db = self.singleton.db
        self.sender = self.singleton.threads["sender"]
        self.list_key = 'gn:alarm:list-alarm'
    def th_exit(self):
        self.__exit = True
    def run(self):
        while not self.__exit:
            if self.db.llen(self.list_key) > 0:
                alarm_list = map(byte2str, self.db.lrange(self.list_key, 0, -1))
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
    def add(self, blist, tm_hour, tm_min, cid, msg):
        alarm = Alarm(blist, tm_hour, tm_min, cid, msg)
        self.db.rpush(self.list_key, str(alarm))
    def add_request(self, msg, args):
        pc = ParseCommand(msg)
        op = pc.op_type()
        if op == '추가':
            self.add(*pc.argpack_add())
            self.sender.add_by_cid_msg(args.chat_id, '추가되었어요')
        elif op == '수정':
            pass
        elif op == '목록':
            l = list(map(byte2str, self.db.lrange(self.list_key, 0, -1)))
            msg = '\n'.join(['%d %s' % (i, j) for i, j in enumerate(l)])
            self.sender.add_by_cid_msg(args.chat_id, msg.replace('@\0@', ' '))
        elif op == '삭제':
            ind = pc.op_index()
            self.db.lset(self.list_key, ind, 'DELETED')
            self.db.lrem(self.list_key, 1, 'DELETED')
            l = list(map(byte2str, self.db.lrange(self.list_key, 0, -1)))
            msg = '\n'.join(['%d %s' % (i, j) for i, j in enumerate(l)])
            self.sender.add_by_cid_msg(args.chat_id, msg.replace('@\0@', ' '))
