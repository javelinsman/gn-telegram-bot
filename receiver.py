import threading
import queue
from types import SimpleNamespace

class ReceiverThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
        self.request_q = queue.Queue()
    def run(self):
        while not self.__exit:
            if not self.request_q.empty():
                args = self.request_q.get()
                self.process_request(args)
    def th_exit(self):
        self.__exit = True
    def add_request(self, args):
        self.request_q.put(args)
    def process_request(self, args):
        new_args = SimpleNamespace()
        new_args.cid = args.chat_id
        new_args.msg = args.text
        self.singleton.threads["sender"].add(new_args)
