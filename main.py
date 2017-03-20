from flask import Flask, request
from receiver import ReceiverThread
from sender import SenderThread
from convert import byte2str
from types import SimpleNamespace
import redis
import json

db = redis.StrictRedis(host='localhost', port=6379, db=0)

bot_config = json.loads(byte2str(db.get('gn:bot-config')))

th_sender = SenderThread()
th_receiver = ReceiverThread()

singleton = SimpleNamespace()
singleton.bot_config = bot_config
singleton.threads = {
    "sender" : th_sender,
    "receiver" : th_receiver,
}

for thread in singleton.threads.values():
    thread.singleton = singleton
    thread.start()

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def webhook():
    print(request.data)
    try:
        data = request.get_json()
        args = SimpleNamespace()
        message = data["message"]
        args.text = message["text"]
        args.chat_id = message["chat"]["id"]
        args.author_id = message["from"]["id"]

        th_receiver.add_request(args)
    except Exception as e:
        print("Error: ", str(e))
    return ''

if __name__ == "__main__":
    try:
        app.run(host=bot_config["host"], port=bot_config["port"], debug=False);
    except (KeyboardInterrupt, SystemExit):
        for thread in singleton.threads.values():
            thread.th_exit()
