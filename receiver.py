import threading
import queue

class ReceiverThread(threading.Thread):
    def __init__(self, th_sender):
        threading.Thread.__init__(self)
        self.__exit = False
        self.th_sender = th_sender
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
        args.send_cid = args.chat_id
        args.send_msg = args.text
        self.th_sender.add(args)
