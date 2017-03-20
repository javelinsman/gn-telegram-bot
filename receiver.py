import threading
import queue
import time
from convert import byte2str
from types import SimpleNamespace

class ReceiverThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
        self.request_q = queue.Queue()
    def __init2__(self):
        self.sender = self.singleton.threads["sender"]
        self.db = self.singleton.db
    def run(self):
        while not self.__exit:
            if not self.request_q.empty():
                args = self.request_q.get()
                self.process_request(args)
            time.sleep(0.1)
    def th_exit(self):
        self.__exit = True
    def add_request(self, args):
        self.request_q.put(args)
    def process_request(self, args):
        if args.text == '.감정기록시작':
            if self.db.sismember('gn:emorec:user-list', args.author_id):
                self.sender.add_by_cid_msg(args.chat_id, '한 번만 말해도 된다냥')
            else:
                self.db.sadd('gn:emorec:user-list', args.author_id)
                self.sender.add_by_cid_msg(args.chat_id, '냥! 잘 부탁해요!')
        elif args.text == '.감정기록그만':
            if self.db.sismember('gn:emorec:user-list', args.author_id):
                self.db.srem('gn:emorec:user-list', args.author_id)
                self.sender.add_by_cid_msg(args.chat_id, '네~ 그동안 재밌었어요 냥')
            else:
                self.sender.add_by_cid_msg(args.chat_id, '한 번만 말해도 된다냥')

        else:
            new_args = SimpleNamespace()
            new_args.cid = args.chat_id
            new_args.msg = args.text
            self.sender.add(new_args)
