import threading
import queue
import requests
import time
from types import SimpleNamespace

import json

class SenderThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__exit = False
        self.request_q = queue.Queue()
    def __init2__(self):
        pass
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
    def add_by_cid_msg(self, cid, msg):
        self.add(SimpleNamespace(cid=cid, msg=msg))

    def send_message(self, cid, text):
        return requests.post(
            self.singleton.bot_config["api_base"] + 'sendMessage',
            data = {
                "chat_id" : cid,
                "text" : text
            })

"""
    "reply_markup" : json.dumps({
        "keyboard" : [
            ["슬픔", "후회", "우울"],
            ["짜증", "화남", "불쾌"],
            ["기쁨", "설렘"],
            ["소소", "보통"],
        ],
        "one_time_keyboard" : True
    })
"""
