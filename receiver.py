import threading
import queue
from types import SimpleNamespace

import time

class ReceiverThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
        self.request_q = queue.Queue()
    def __init2__(self):
        self.sender = self.singleton.threads["sender"]
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
        new_args = SimpleNamespace()
        new_args.cid = args.chat_id
        new_args.msg = args.text
        self.sender.add(new_args)
