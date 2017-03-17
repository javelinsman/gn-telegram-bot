import threading
import queue
import requests
import time

class SenderThread(threading.Thread):
    def __init__(self, bot_config):
        threading.Thread.__init__(self)
        self.__exit = False
        self.request_q = queue.Queue()
        self.bot_config = bot_config
    def th_exit(self):
        self.__exit = True
    def run(self):
        while not self.__exit:
            if not self.request_q.empty():
                args = self.request_q.get()
                self.send_message(args.send_cid, args.send_msg)
                time.sleep(1)
    def add(self, args):
        self.request_q.put(args)

    def send_message(self, cid, text):
        return requests.post(
            self.bot_config["api_base"] + 'sendMessage',
            data = {
                "chat_id" : cid,
                "text" : text
            })

