import threading
import queue
import requests
import time

class SenderThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
        self.request_q = queue.Queue()
    def th_exit(self):
        self.__exit = True
    def run(self):
        while not self.__exit:
            if not self.request_q.empty():
                args = self.request_q.get()
                self.send_message(args.cid, args.msg)
                time.sleep(1)
    def add(self, args):
        self.request_q.put(args)

    def send_message(self, cid, text):
        return requests.post(
            self.singleton.bot_config["api_base"] + 'sendMessage',
            data = {
                "chat_id" : cid,
                "text" : text
            })

