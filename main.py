from flask import Flask, request
from receiver import ReceiverThread
from sender import SenderThread

import json
bot_config = None
with open('bot_config.json', 'r') as f:
    bot_config = json.loads(f.read())

class Args:
    pass


th_sender = SenderThread(bot_config)
th_sender.start()
th_receiver = ReceiverThread(th_sender)
th_receiver.start()

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def webhook():
    print(request.data)
    try:
        data = request.get_json()
        args = Args()
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
        th_receiver.th_exit()
        th_sender.th_exit()


